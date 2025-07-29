#!/usr/bin/env python
"""
샘플 데이터 생성 스크립트
헬스장 회원관리 시스템의 테스트를 위한 샘플 데이터를 생성합니다.
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
from decimal import Decimal
import random
from django.utils import timezone

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamood_gym.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.branches.models import Branch, BranchAdmin
from apps.members.models import Member, PTProgram, MemberPTRegistration
from apps.trainers.models import Trainer, TrainerIncentive, TrainerSchedule, TrainerBlockedTime
from apps.reservations.models import Reservation, PTRecord, ReservationChangeLog
from apps.salaries.models import Salary, IncentiveDetail, BranchRevenue
from apps.notifications.models import Notification, NotificationTemplate
from apps.dashboards.models import DashboardWidget, DashboardLayout, UserDashboard

User = get_user_model()


def create_branches():
    """지점 데이터 생성"""
    print("지점 데이터 생성 중...")
    
    branches_data = [
        {
            'name': '강남점',
            'address': '서울특별시 강남구 테헤란로 123',
            'phone': '02-1234-5678',
            'email': 'gangnam@clamood.com'
        },
        {
            'name': '홍대점',
            'address': '서울특별시 마포구 홍대로 456',
            'phone': '02-2345-6789',
            'email': 'hongdae@clamood.com'
        },
        {
            'name': '부산점',
            'address': '부산광역시 해운대구 해운대로 789',
            'phone': '051-3456-7890',
            'email': 'busan@clamood.com'
        }
    ]
    
    branches = []
    for data in branches_data:
        branch, created = Branch.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        branches.append(branch)
        if created:
            print(f"지점 생성: {branch.name}")
    
    return branches


def create_admins(branches):
    """어드민 데이터 생성"""
    print("어드민 데이터 생성 중...")
    
    # 본사 어드민
    headquarters_admin, created = BranchAdmin.objects.get_or_create(
        username='headquarters_admin',
        defaults={
            'email': 'headquarters@clamood.com',
            'first_name': '본사',
            'last_name': '관리자',
            'admin_type': 'headquarters',
            'phone': '010-0000-0000',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        headquarters_admin.set_password('password123')
        headquarters_admin.save()
        print("본사 어드민 생성")
    
    # 지점별 어드민
    for i, branch in enumerate(branches):
        admin, created = BranchAdmin.objects.get_or_create(
            username=f'branch_admin_{i+1}',
            defaults={
                'email': f'branch{i+1}@clamood.com',
                'first_name': f'{branch.name}',
                'last_name': '관리자',
                'branch': branch,
                'admin_type': 'branch',
                'phone': f'010-{1000+i:04d}-{1000+i:04d}',
                'is_staff': True
            }
        )
        if created:
            admin.set_password('password123')
            admin.save()
            print(f"지점 어드민 생성: {branch.name}")


def create_pt_programs(branches):
    """PT 프로그램 데이터 생성"""
    print("PT 프로그램 데이터 생성 중...")
    
    programs_data = [
        {
            'name': '신규 회원 PT',
            'program_type': 'new',
            'sessions': 10,
            'price': Decimal('500000'),
            'description': '신규 회원을 위한 기본 PT 프로그램'
        },
        {
            'name': '장기 PT',
            'program_type': 'long_term',
            'sessions': 30,
            'price': Decimal('1200000'),
            'description': '장기간 지속적인 관리를 위한 PT 프로그램'
        },
        {
            'name': '단기 집중 PT',
            'program_type': 'short_term',
            'sessions': 5,
            'price': Decimal('300000'),
            'description': '단기간 집중적인 관리를 위한 PT 프로그램'
        }
    ]
    
    programs = []
    for branch in branches:
        for data in programs_data:
            program, created = PTProgram.objects.get_or_create(
                branch=branch,
                name=data['name'],
                defaults=data
            )
            programs.append(program)
            if created:
                print(f"PT 프로그램 생성: {branch.name} - {program.name}")
    
    return programs


def create_trainers(branches):
    """트레이너 데이터 생성"""
    print("트레이너 데이터 생성 중...")
    
    trainers_data = [
        {
            'name': '김철수',
            'phone': '010-1111-1111',
            'email': 'trainer1@clamood.com',
            'gender': 'M',
            'base_salary': Decimal('2500000'),
            'kakao_id': 'trainer_kim',
            'specialties': '웨이트 트레이닝, 다이어트',
            'certifications': '생활스포츠지도사 2급',
            'experience_years': 3
        },
        {
            'name': '이영희',
            'phone': '010-2222-2222',
            'email': 'trainer2@clamood.com',
            'gender': 'F',
            'base_salary': Decimal('2200000'),
            'kakao_id': 'trainer_lee',
            'specialties': '요가, 필라테스',
            'certifications': '요가지도사, 필라테스 지도사',
            'experience_years': 5
        },
        {
            'name': '박민수',
            'phone': '010-3333-3333',
            'email': 'trainer3@clamood.com',
            'gender': 'M',
            'base_salary': Decimal('2800000'),
            'kakao_id': 'trainer_park',
            'specialties': '크로스핏, 기능성 운동',
            'certifications': '크로스핏 레벨 1, 기능성 운동 전문가',
            'experience_years': 7
        }
    ]
    
    trainers = []
    for i, branch in enumerate(branches):
        for j, data in enumerate(trainers_data):
            trainer, created = Trainer.objects.get_or_create(
                branch=branch,
                name=f"{data['name']} ({branch.name})",
                defaults={
                    **data,
                    'hire_date': date.today() - timedelta(days=random.randint(365, 1095)),
                    'birth_date': date(1990 + random.randint(0, 10), random.randint(1, 12), random.randint(1, 28))
                }
            )
            trainers.append(trainer)
            if created:
                print(f"트레이너 생성: {trainer.name}")
    
    return trainers


def create_trainer_incentives(trainers):
    """트레이너 인센티브 설정"""
    print("트레이너 인센티브 설정 중...")
    
    for trainer in trainers:
        incentive, created = TrainerIncentive.objects.get_or_create(
            trainer=trainer,
            defaults={
                'incentive_type': random.choice(['fixed', 'percentage']),
                'fixed_amount': Decimal('50000') if random.choice([True, False]) else Decimal('0'),
                'percentage_rate': Decimal('10.0') if random.choice([True, False]) else Decimal('0')
            }
        )
        if created:
            print(f"인센티브 설정: {trainer.name}")


def create_trainer_schedules(trainers):
    """트레이너 일정 설정"""
    print("트레이너 일정 설정 중...")
    
    for trainer in trainers:
        for day in range(7):  # 월요일부터 일요일까지
            schedule, created = TrainerSchedule.objects.get_or_create(
                trainer=trainer,
                day_of_week=day,
                defaults={
                    'start_time': '09:00',
                    'end_time': '18:00',
                    'is_available': day < 6  # 일요일은 휴무
                }
            )
            if created:
                print(f"일정 설정: {trainer.name} - {schedule.get_day_of_week_display()}")


def create_members(branches, programs):
    """회원 데이터 생성"""
    print("회원 데이터 생성 중...")
    
    members_data = [
        {'name': '김회원', 'gender': 'M'},
        {'name': '이회원', 'gender': 'F'},
        {'name': '박회원', 'gender': 'M'},
        {'name': '최회원', 'gender': 'F'},
        {'name': '정회원', 'gender': 'M'},
        {'name': '한회원', 'gender': 'F'},
        {'name': '윤회원', 'gender': 'M'},
        {'name': '임회원', 'gender': 'F'},
    ]
    
    members = []
    for branch in branches:
        for i, data in enumerate(members_data):
            member, created = Member.objects.get_or_create(
                branch=branch,
                name=f"{data['name']}{i+1}",
                defaults={
                    'phone': f'010-{4000+i:04d}-{4000+i:04d}',
                    'email': f'member{i+1}@example.com',
                    'gender': data['gender'],
                    'birth_date': date(1980 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28)),
                    'address': f'{branch.name} 근처 주소',
                    'emergency_contact': f'010-{5000+i:04d}-{5000+i:04d}',
                    'membership_status': random.choice(['active', 'active', 'active', 'inactive']),
                    'registration_date': date.today() - timedelta(days=random.randint(30, 365))
                }
            )
            members.append(member)
            if created:
                print(f"회원 생성: {member.name} ({branch.name})")
    
    return members


def create_pt_registrations(members, programs, trainers):
    """PT 등록 데이터 생성"""
    print("PT 등록 데이터 생성 중...")
    
    registrations = []
    for member in members:
        if member.membership_status == 'active':
            # 70% 확률로 PT 등록
            if random.random() < 0.7:
                program = random.choice(programs)
                trainer = random.choice([t for t in trainers if t.branch == member.branch])
                
                registration, created = MemberPTRegistration.objects.get_or_create(
                    member=member,
                    pt_program=program,
                    defaults={
                        'trainer': trainer,
                        'total_sessions': program.sessions,
                        'remaining_sessions': program.sessions - random.randint(0, program.sessions // 2),
                        'total_price': program.price,
                        'paid_amount': program.price,
                        'registration_status': 'active',
                        'registration_date': member.registration_date + timedelta(days=random.randint(1, 30)),
                        'expiry_date': date.today() + timedelta(days=random.randint(30, 180))
                    }
                )
                registrations.append(registration)
                if created:
                    print(f"PT 등록 생성: {member.name} - {program.name}")
    
    return registrations


def create_reservations(members, trainers, registrations):
    """예약 데이터 생성"""
    print("예약 데이터 생성 중...")
    
    reservations = []
    for member in members:
        if member.membership_status == 'active':
            # 회원의 PT 등록 찾기
            member_registrations = [r for r in registrations if r.member == member]
            
            for registration in member_registrations:
                # 과거 30일간의 예약 생성
                for i in range(random.randint(3, 8)):
                    reservation_date = date.today() - timedelta(days=random.randint(1, 30))
                    
                    # 트레이너의 근무 시간 확인
                    trainer = registration.trainer
                    day_of_week = reservation_date.weekday()
                    
                    try:
                        schedule = TrainerSchedule.objects.get(
                            trainer=trainer,
                            day_of_week=day_of_week,
                            is_available=True
                        )
                        
                        # 근무 시간 내에서 랜덤 시간 선택
                        start_hour = random.randint(9, 17)
                        start_time = f"{start_hour:02d}:{random.choice(['00', '30'])}"
                        
                        reservation, created = Reservation.objects.get_or_create(
                            member=member,
                            trainer=trainer,
                            pt_registration=registration,
                            date=reservation_date,
                            start_time=start_time,
                            defaults={
                                'duration': 30,
                                'reservation_status': random.choice(['completed', 'completed', 'confirmed', 'pending']),
                                'notes': f'샘플 예약 {i+1}'
                            }
                        )
                        
                        if created:
                            reservations.append(reservation)
                            print(f"예약 생성: {member.name} - {trainer.name} ({reservation_date})")
                            
                            # 완료된 예약의 경우 PT 기록 생성
                            if reservation.reservation_status == 'completed':
                                pt_record, created = PTRecord.objects.get_or_create(
                                    reservation=reservation,
                                    defaults={
                                        'trainer': trainer,
                                        'member': member,
                                        'workout_date': reservation_date,
                                        'workout_time': reservation.start_time,
                                        'duration': reservation.duration,
                                        'content': f'샘플 PT 내용 - {random.choice(["웨이트 트레이닝", "유산소 운동", "스트레칭", "기능성 운동"])}',
                                        'member_condition': '양호',
                                        'trainer_notes': f'샘플 트레이너 메모 {i+1}',
                                        'is_completed': True
                                    }
                                )
                                if created:
                                    print(f"PT 기록 생성: {member.name} - {trainer.name}")
                        
                    except TrainerSchedule.DoesNotExist:
                        continue
    
    return reservations


def create_salaries(trainers):
    """급여 데이터 생성"""
    print("급여 데이터 생성 중...")
    
    current_year = date.today().year
    current_month = date.today().month
    
    for trainer in trainers:
        # 최근 3개월 급여 생성
        for i in range(3):
            calc_month = current_month - i
            calc_year = current_year
            
            if calc_month <= 0:
                calc_month += 12
                calc_year -= 1
            
            salary, created = Salary.objects.get_or_create(
                trainer=trainer,
                year=calc_year,
                month=calc_month,
                defaults={
                    'base_salary': trainer.base_salary,
                    'incentive_amount': Decimal(random.randint(50000, 200000)),
                    'additional_revenue': Decimal(random.randint(0, 100000)),
                    'other_costs': Decimal(random.randint(0, 50000)),
                    'payment_status': 'paid',
                    'payment_date': date(calc_year, calc_month, 25)
                }
            )
            
            if created:
                print(f"급여 생성: {trainer.name} - {calc_year}년 {calc_month}월")


def create_branch_revenues(branches):
    """지점 매출 데이터 생성"""
    print("지점 매출 데이터 생성 중...")
    
    current_year = date.today().year
    current_month = date.today().month
    
    for branch in branches:
        # 최근 6개월 매출 생성
        for i in range(6):
            calc_month = current_month - i
            calc_year = current_year
            
            if calc_month <= 0:
                calc_month += 12
                calc_year -= 1
            
            revenue, created = BranchRevenue.objects.get_or_create(
                branch=branch,
                year=calc_year,
                month=calc_month,
                defaults={
                    'pt_revenue': Decimal(random.randint(5000000, 15000000)),
                    'membership_revenue': Decimal(random.randint(2000000, 8000000)),
                    'additional_revenue': Decimal(random.randint(500000, 2000000))
                }
            )
            
            if created:
                print(f"매출 생성: {branch.name} - {calc_year}년 {calc_month}월")


def create_notifications(members, trainers, reservations):
    """알림 데이터 생성"""
    print("알림 데이터 생성 중...")
    
    # 알림 템플릿 생성
    templates_data = [
        {
            'name': '예약 요청 템플릿',
            'notification_type': 'reservation_request',
            'title_template': '새로운 PT 예약 요청',
            'message_template': '{member_name} 회원님이 {date} {time}에 PT 예약을 요청했습니다.'
        },
        {
            'name': '예약 확정 템플릿',
            'notification_type': 'reservation_confirmed',
            'title_template': 'PT 예약이 확정되었습니다',
            'message_template': '{date} {time} PT 예약이 확정되었습니다.'
        },
        {
            'name': 'PT 완료 템플릿',
            'notification_type': 'pt_completed',
            'title_template': 'PT 세션이 완료되었습니다',
            'message_template': '{member_name} 회원님의 PT 세션이 성공적으로 완료되었습니다.'
        }
    ]
    
    for data in templates_data:
        template, created = NotificationTemplate.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"알림 템플릿 생성: {template.name}")
    
    # 샘플 알림 생성
    for i in range(20):
        notification_type = random.choice(['reservation_request', 'reservation_confirmed', 'pt_completed', 'system'])
        
        if notification_type in ['reservation_request', 'reservation_confirmed', 'pt_completed'] and reservations:
            reservation = random.choice(reservations)
            recipient_type = 'trainer' if notification_type == 'reservation_request' else 'member'
            recipient_id = reservation.trainer.id if recipient_type == 'trainer' else reservation.member.id
        else:
            # 시스템 알림
            recipient_type = random.choice(['member', 'trainer'])
            if recipient_type == 'member':
                recipient_id = random.choice(members).id
            else:
                recipient_id = random.choice(trainers).id
        
        notification, created = Notification.objects.get_or_create(
            notification_type=notification_type,
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            title=f'샘플 알림 {i+1}',
            defaults={
                'message': f'이것은 샘플 알림 메시지 {i+1}입니다.',
                'priority': random.choice(['low', 'medium', 'high']),
                'status': random.choice(['sent', 'read']),
                'kakao_sent': random.choice([True, False]),
                'created_at': timezone.now() - timedelta(days=random.randint(1, 30))
            }
        )
        
        if created:
            print(f"알림 생성: {notification.title}")


def create_dashboard_widgets():
    """대시보드 위젯 생성"""
    print("대시보드 위젯 생성 중...")
    
    widgets_data = [
        {
            'name': '전체 통계',
            'widget_type': 'metric_card',
            'title': '전체 통계',
            'description': '회원, 트레이너, 예약, 매출 통계',
            'data_source': 'overview_statistics'
        },
        {
            'name': '매출 차트',
            'widget_type': 'revenue_chart',
            'chart_type': 'line',
            'title': '매출 추이',
            'description': '월별 매출 추이 차트',
            'data_source': 'revenue_statistics'
        },
        {
            'name': '예약 현황',
            'widget_type': 'reservation_stats',
            'chart_type': 'bar',
            'title': '예약 현황',
            'description': '일별 예약 현황 차트',
            'data_source': 'reservation_statistics'
        }
    ]
    
    for data in widgets_data:
        widget, created = DashboardWidget.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"대시보드 위젯 생성: {widget.name}")


def main():
    """메인 실행 함수"""
    print("=== 헬스장 회원관리 시스템 샘플 데이터 생성 ===")
    
    try:
        # 1. 지점 생성
        branches = create_branches()
        
        # 2. 어드민 생성
        create_admins(branches)
        
        # 3. PT 프로그램 생성
        programs = create_pt_programs(branches)
        
        # 4. 트레이너 생성
        trainers = create_trainers(branches)
        create_trainer_incentives(trainers)
        create_trainer_schedules(trainers)
        
        # 5. 회원 생성
        members = create_members(branches, programs)
        
        # 6. PT 등록 생성
        registrations = create_pt_registrations(members, programs, trainers)
        
        # 7. 예약 생성
        reservations = create_reservations(members, trainers, registrations)
        
        # 8. 급여 데이터 생성
        create_salaries(trainers)
        
        # 9. 지점 매출 데이터 생성
        create_branch_revenues(branches)
        
        # 10. 알림 데이터 생성
        create_notifications(members, trainers, reservations)
        
        # 11. 대시보드 위젯 생성
        create_dashboard_widgets()
        
        print("\n=== 샘플 데이터 생성 완료 ===")
        print(f"생성된 데이터:")
        print(f"- 지점: {len(branches)}개")
        print(f"- 트레이너: {len(trainers)}명")
        print(f"- 회원: {len(members)}명")
        print(f"- PT 등록: {len(registrations)}건")
        print(f"- 예약: {len(reservations)}건")
        print(f"- PT 프로그램: {len(programs)}개")
        
        print("\n기본 로그인 정보:")
        print("본사 어드민: headquarters_admin / password123")
        print("지점 어드민: branch_admin_1 / password123")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main() 