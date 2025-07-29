import logging
from datetime import datetime, date, timedelta
from celery import shared_task
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from apps.notifications.models import Notification, NotificationTemplate, NotificationLog
from apps.reservations.models import Reservation, PTRecord
from apps.trainers.models import Trainer
from apps.members.models import Member
from apps.salaries.models import Salary, BranchRevenue
from apps.salaries.services import salary_calculation_service, branch_revenue_service
from apps.members.models import MemberPTRegistration
from apps.dashboards.services import dashboard_service
from apps.notifications.services import notification_service


logger = logging.getLogger(__name__)


@shared_task
def send_reservation_reminders():
    """예약 알림 전송 태스크 (매일 실행)"""
    tomorrow = timezone.now().date() + timedelta(days=1)
    
    # 내일 예약이 있는 확정된 예약들 조회
    reservations = Reservation.objects.filter(
        date=tomorrow,
        reservation_status='confirmed'
    )
    
    sent_count = 0
    for reservation in reservations:
        try:
            # 트레이너에게 알림
            notification_service.send_reservation_notification(
                reservation=reservation,
                notification_type='reservation_reminder',
                recipient_type='trainer',
                recipient_id=reservation.trainer.id
            )
            
            # 회원에게 알림
            notification_service.send_reservation_notification(
                reservation=reservation,
                notification_type='reservation_reminder',
                recipient_type='member',
                recipient_id=reservation.member.id
            )
            
            sent_count += 1
        except Exception as e:
            print(f"예약 알림 전송 실패 (예약 ID: {reservation.id}): {str(e)}")
    
    return f"예약 알림 {sent_count}건 전송 완료"


@shared_task
def send_daily_notifications():
    """일일 알림 전송 태스크"""
    today = timezone.now().date()
    
    # 오늘 PT 세션이 있는 회원들에게 알림
    reservations = Reservation.objects.filter(
        date=today,
        reservation_status='confirmed'
    )
    
    for reservation in reservations:
        # PT 시작 1시간 전 알림
        start_time = datetime.combine(today, reservation.start_time)
        if start_time - timezone.now() <= timedelta(hours=1):
            notification_service.send_reservation_notification(
                reservation=reservation,
                notification_type='reservation_reminder',
                recipient_type='member',
                recipient_id=reservation.member.id
            )


@shared_task
def calculate_monthly_salaries(year=None, month=None):
    """월별 급여 계산 태스크 (매월 1일 실행)"""
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().month
    
    # 이전 달 급여 계산
    if month == 1:
        calc_year = year - 1
        calc_month = 12
    else:
        calc_year = year
        calc_month = month - 1
    
    try:
        salaries = salary_calculation_service.calculate_all_trainers_salary(calc_year, calc_month)
        
        # 급여 지급 알림 전송
        for salary in salaries:
            if salary.total_salary > 0:
                notification_service.send_salary_notification(salary)
        
        return f"{calc_year}년 {calc_month}월 급여 계산 완료 ({len(salaries)}명)"
    except Exception as e:
        return f"급여 계산 실패: {str(e)}"


@shared_task
def calculate_monthly_revenues(year=None, month=None):
    """월별 매출 계산 태스크 (매월 1일 실행)"""
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().month
    
    # 이전 달 매출 계산
    if month == 1:
        calc_year = year - 1
        calc_month = 12
    else:
        calc_year = year
        calc_month = month - 1
    
    try:
        revenues = branch_revenue_service.calculate_all_branches_revenue(calc_year, calc_month)
        return f"{calc_year}년 {calc_month}월 매출 계산 완료 ({len(revenues)}개 지점)"
    except Exception as e:
        return f"매출 계산 실패: {str(e)}"


@shared_task
def cleanup_old_notifications():
    """오래된 알림 정리 태스크 (매주 실행)"""
    # 3개월 이상 된 읽은 알림 삭제
    cutoff_date = timezone.now() - timedelta(days=90)
    
    deleted_count = Notification.objects.filter(
        read_at__lt=cutoff_date,
        status='read'
    ).delete()[0]
    
    return f"오래된 알림 {deleted_count}건 삭제 완료"


@shared_task
def retry_failed_notifications():
    """실패한 알림 재전송 태스크 (매시간 실행)"""
    # 전송 실패한 알림들 재시도
    failed_notifications = Notification.objects.filter(
        status='failed',
        created_at__gte=timezone.now() - timedelta(days=1)  # 최근 24시간 내
    )
    
    retry_count = 0
    for notification in failed_notifications:
        try:
            success = notification_service.send_notification(notification)
            if success:
                retry_count += 1
        except Exception as e:
            print(f"알림 재전송 실패 (알림 ID: {notification.id}): {str(e)}")
    
    return f"실패한 알림 {retry_count}건 재전송 완료"


@shared_task
def send_weekly_reports():
    """주간 리포트 전송 태스크 (매주 월요일 실행)"""
    
    # 지난 주 통계 생성
    end_date = timezone.now().date() - timedelta(days=1)  # 어제
    start_date = end_date - timedelta(days=6)  # 7일 전
    
    try:
        # 각 지점별 주간 리포트 생성
        from apps.branches.models import Branch
        
        for branch in Branch.objects.filter(is_active=True):
            # 지점 어드민들에게 주간 리포트 전송
            branch_admins = branch.branchadmin_set.filter(is_active=True)
            
            for admin in branch_admins:
                # 주간 통계 데이터 생성
                weekly_stats = dashboard_service.get_weekly_statistics(
                    branch_id=branch.id,
                    start_date=start_date,
                    end_date=end_date
                )
                
                # 리포트 알림 전송
                notification_service.create_notification(
                    notification_type='system',
                    recipient_type='admin',
                    recipient_id=admin.id,
                    title=f"{branch.name} 주간 리포트",
                    message=f"지난 주 통계: 회원 {weekly_stats.get('new_members', 0)}명 신규 등록, "
                           f"PT 예약 {weekly_stats.get('total_reservations', 0)}건, "
                           f"매출 {weekly_stats.get('total_revenue', 0):,}원"
                )
        
        return "주간 리포트 전송 완료"
    except Exception as e:
        return f"주간 리포트 전송 실패: {str(e)}"


@shared_task
def send_monthly_reports():
    """월간 리포트 전송 태스크 (매월 1일 실행)"""
    
    # 지난 달 통계
    today = timezone.now().date()
    if today.month == 1:
        last_month = 12
        last_year = today.year - 1
    else:
        last_month = today.month - 1
        last_year = today.year
    
    try:
        # 본사 어드민들에게 월간 리포트 전송
        from apps.branches.models import BranchAdmin
        
        headquarters_admins = BranchAdmin.objects.filter(
            admin_type='headquarters',
            is_active=True
        )
        
        for admin in headquarters_admins:
            # 전체 지점 월간 통계
            monthly_stats = dashboard_service.get_monthly_statistics(
                year=last_year,
                month=last_month
            )
            
            notification_service.create_notification(
                notification_type='system',
                recipient_type='admin',
                recipient_id=admin.id,
                title=f"{last_year}년 {last_month}월 월간 리포트",
                message=f"전체 지점 통계: 회원 {monthly_stats.get('total_members', 0)}명, "
                       f"PT 예약 {monthly_stats.get('total_reservations', 0)}건, "
                       f"총 매출 {monthly_stats.get('total_revenue', 0):,}원"
            )
        
        return "월간 리포트 전송 완료"
    except Exception as e:
        return f"월간 리포트 전송 실패: {str(e)}"


@shared_task
def check_expiring_pt_registrations():
    """만료 예정 PT 등록 확인 태스크 (매일 실행)"""
    # 7일 후 만료되는 PT 등록 확인
    expiry_date = timezone.now().date() + timedelta(days=7)
    
    expiring_registrations = MemberPTRegistration.objects.filter(
        expiry_date=expiry_date,
        registration_status='active'
    )
    
    for registration in expiring_registrations:
        # 회원에게 만료 알림
        notification_service.create_notification(
            notification_type='system',
            recipient_type='member',
            recipient_id=registration.member.id,
            title="PT 등록 만료 예정",
            message=f"{registration.pt_program.name} 등록이 {expiry_date}에 만료됩니다. "
                   f"남은 횟수: {registration.remaining_sessions}회"
        )
        
        # 담당 트레이너에게도 알림
        if registration.trainer:
            notification_service.create_notification(
                notification_type='system',
                recipient_type='trainer',
                recipient_id=registration.trainer.id,
                title="회원 PT 등록 만료 예정",
                message=f"{registration.member.name} 회원님의 {registration.pt_program.name} "
                       f"등록이 {expiry_date}에 만료됩니다."
            )


@shared_task
def update_expired_pt_registrations():
    """만료된 PT 등록 상태 업데이트 태스크 (매일 실행)"""
    
    # 만료된 PT 등록 상태 변경
    expired_count = MemberPTRegistration.objects.filter(
        expiry_date__lt=timezone.now().date(),
        registration_status='active'
    ).update(registration_status='expired')
    
    return f"만료된 PT 등록 {expired_count}건 상태 업데이트 완료"


@shared_task
def send_birthday_notifications():
    """생일 알림 전송 태스크 (매일 실행)"""
    today = timezone.now().date()
    
    # 오늘 생일인 회원들 조회
    from apps.members.models import Member
    
    birthday_members = Member.objects.filter(
        birth_date__month=today.month,
        birth_date__day=today.day,
        membership_status='active'
    )
    
    for member in birthday_members:
        # 생일 축하 알림
        notification_service.create_notification(
            notification_type='system',
            recipient_type='member',
            recipient_id=member.id,
            title="생일 축하합니다! 🎉",
            message=f"{member.name}님, 생일을 진심으로 축하드립니다! "
                   f"오늘도 건강한 하루 되세요!"
        )
        
        # 담당 트레이너에게도 알림
        pt_registrations = member.memberptregistration_set.filter(
            registration_status='active',
            trainer__isnull=False
        )
        
        for registration in pt_registrations:
            notification_service.create_notification(
                notification_type='system',
                recipient_type='trainer',
                recipient_id=registration.trainer.id,
                title="회원 생일 알림",
                message=f"{member.name} 회원님의 생일입니다. "
                       f"특별한 PT 세션을 준비해보세요!"
            ) 


@shared_task
def send_reservation_request_notification(reservation_id):
    """예약 요청 알림 전송"""
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        
        # 트레이너에게 예약 요청 알림
        notification_service.create_notification(
            notification_type='reservation_request',
            recipient_type='trainer',
            recipient_id=reservation.trainer.id,
            title="새로운 PT 예약 요청",
            message=f"{reservation.member.name} 회원님이 {reservation.date} {reservation.start_time}에 PT 예약을 요청했습니다."
        )
        
        return f"예약 요청 알림 전송 완료 (예약 ID: {reservation_id})"
    except Reservation.DoesNotExist:
        return f"예약을 찾을 수 없습니다 (ID: {reservation_id})"
    except Exception as e:
        return f"예약 요청 알림 전송 실패: {str(e)}"


@shared_task
def send_reservation_status_notification(reservation_id, new_status):
    """예약 상태 변경 알림 전송"""
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        
        status_messages = {
            'confirmed': '예약이 확정되었습니다.',
            'rejected': '예약이 거절되었습니다.',
            'cancelled': '예약이 취소되었습니다.',
            'completed': 'PT 세션이 완료되었습니다.'
        }
        
        message = status_messages.get(new_status, f'예약 상태가 {new_status}로 변경되었습니다.')
        
        # 회원에게 상태 변경 알림
        notification_service.create_notification(
            notification_type=f'reservation_{new_status}',
            recipient_type='member',
            recipient_id=reservation.member.id,
            title="PT 예약 상태 변경",
            message=f"{reservation.date} {reservation.start_time} 예약이 {message}"
        )
        
        return f"예약 상태 변경 알림 전송 완료 (예약 ID: {reservation_id}, 상태: {new_status})"
    except Reservation.DoesNotExist:
        return f"예약을 찾을 수 없습니다 (ID: {reservation_id})"
    except Exception as e:
        return f"예약 상태 변경 알림 전송 실패: {str(e)}"


@shared_task
def send_pt_completion_notification(pt_record_id):
    """PT 완료 알림 전송"""
    try:
        pt_record = PTRecord.objects.get(id=pt_record_id)
        
        # 회원에게 PT 완료 알림
        notification_service.create_notification(
            notification_type='pt_completed',
            recipient_type='member',
            recipient_id=pt_record.member.id,
            title="PT 세션 완료",
            message=f"{pt_record.workout_date} PT 세션이 완료되었습니다. 수고하셨습니다!"
        )
        
        # 트레이너에게도 알림
        notification_service.create_notification(
            notification_type='pt_completed',
            recipient_type='trainer',
            recipient_id=pt_record.trainer.id,
            title="PT 세션 완료",
            message=f"{pt_record.member.name} 회원님의 PT 세션이 완료되었습니다."
        )
        
        return f"PT 완료 알림 전송 완료 (PT 기록 ID: {pt_record_id})"
    except PTRecord.DoesNotExist:
        return f"PT 기록을 찾을 수 없습니다 (ID: {pt_record_id})"
    except Exception as e:
        return f"PT 완료 알림 전송 실패: {str(e)}" 