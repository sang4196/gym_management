import logging
from datetime import datetime, date
from decimal import Decimal
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from apps.salaries.models import Salary, IncentiveDetail, AdditionalRevenue, OtherCost
from apps.trainers.models import Trainer, TrainerIncentive
from apps.reservations.models import Reservation, PTRecord
from apps.members.models import MemberPTRegistration


logger = logging.getLogger(__name__)


@shared_task
def calculate_monthly_salaries(year=None, month=None):
    """월별 급여 자동 계산"""
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().month
    
    logger.info(f"급여 계산 시작: {year}년 {month}월")
    
    try:
        with transaction.atomic():
            # 모든 활성 트레이너 조회
            trainers = Trainer.objects.filter(employment_status='active')
            
            for trainer in trainers:
                # 기존 급여 기록이 있는지 확인
                salary, created = Salary.objects.get_or_create(
                    trainer=trainer,
                    year=year,
                    month=month,
                    defaults={
                        'base_salary': trainer.base_salary,
                        'incentive_amount': Decimal('0'),
                        'additional_revenue': Decimal('0'),
                        'other_costs': Decimal('0'),
                    }
                )
                
                if not created:
                    # 기존 인센티브, 추가매출, 기타비용 삭제
                    salary.incentive_details.all().delete()
                    salary.additional_revenues.all().delete()
                    salary.other_cost_items.all().delete()
                
                # 인센티브 계산
                incentive_amount = calculate_trainer_incentive(trainer, year, month)
                salary.incentive_amount = incentive_amount
                
                # 추가매출 계산
                additional_revenue = calculate_additional_revenue(trainer, year, month)
                salary.additional_revenue = additional_revenue
                
                # 기타비용 계산
                other_costs = calculate_other_costs(trainer, year, month)
                salary.other_costs = other_costs
                
                # 총 급여 계산 및 저장
                salary.save()
                
                logger.info(f"트레이너 {trainer.name} 급여 계산 완료: {salary.total_salary}원")
        
        logger.info(f"급여 계산 완료: {year}년 {month}월")
        return True
        
    except Exception as e:
        logger.error(f"급여 계산 중 오류 발생: {str(e)}")
        return False


def calculate_trainer_incentive(trainer, year, month):
    """트레이너 인센티브 계산"""
    try:
        incentive_setting = TrainerIncentive.objects.get(trainer=trainer, is_active=True)
    except TrainerIncentive.DoesNotExist:
        return Decimal('0')
    
    # 해당 월의 완료된 PT 세션 수 조회
    completed_sessions = PTRecord.objects.filter(
        trainer=trainer,
        workout_date__year=year,
        workout_date__month=month,
        is_completed=True
    ).count()
    
    if incentive_setting.incentive_type == 'fixed':
        # 고정 금액: PT 세션당 고정 금액
        return incentive_setting.fixed_amount * completed_sessions
    else:
        # 퍼센티지: 해당 월 PT 매출의 퍼센티지
        pt_revenue = calculate_pt_revenue(trainer, year, month)
        return (pt_revenue * incentive_setting.percentage_rate) / 100


def calculate_pt_revenue(trainer, year, month):
    """PT 매출 계산"""
    # 해당 월에 완료된 PT 세션의 매출 계산
    pt_records = PTRecord.objects.filter(
        trainer=trainer,
        workout_date__year=year,
        workout_date__month=month,
        is_completed=True
    )
    
    total_revenue = Decimal('0')
    for pt_record in pt_records:
        # PT 등록에서 세션당 가격 계산
        if pt_record.reservation.pt_registration:
            pt_registration = pt_record.reservation.pt_registration
            session_price = pt_registration.total_price / pt_registration.total_sessions
            total_revenue += session_price
    
    return total_revenue


def calculate_additional_revenue(trainer, year, month):
    """추가매출 계산 (보충제, 운동용품 등)"""
    # 실제 구현에서는 추가매출 데이터를 별도로 관리해야 함
    # 현재는 기본값 0으로 설정
    return Decimal('0')


def calculate_other_costs(trainer, year, month):
    """기타비용 계산 (보험료, 세금 등)"""
    # 실제 구현에서는 기타비용 데이터를 별도로 관리해야 함
    # 현재는 기본값 0으로 설정
    return Decimal('0')


@shared_task
def update_branch_revenue():
    """지점별 매출 업데이트"""
    from apps.salaries.models import BranchRevenue
    
    logger.info("지점별 매출 업데이트 시작")
    
    try:
        with transaction.atomic():
            current_date = timezone.now().date()
            year = current_date.year
            month = current_date.month
            
            from apps.branches.models import Branch
            branches = Branch.objects.filter(is_active=True)
            
            for branch in branches:
                # PT 매출 계산
                pt_revenue = calculate_branch_pt_revenue(branch, year, month)
                
                # 회원권 매출 계산
                membership_revenue = calculate_branch_membership_revenue(branch, year, month)
                
                # 추가 매출 계산
                additional_revenue = calculate_branch_additional_revenue(branch, year, month)
                
                # 지점 매출 업데이트 또는 생성
                branch_revenue, created = BranchRevenue.objects.get_or_create(
                    branch=branch,
                    year=year,
                    month=month,
                    defaults={
                        'pt_revenue': pt_revenue,
                        'membership_revenue': membership_revenue,
                        'additional_revenue': additional_revenue,
                    }
                )
                
                if not created:
                    branch_revenue.pt_revenue = pt_revenue
                    branch_revenue.membership_revenue = membership_revenue
                    branch_revenue.additional_revenue = additional_revenue
                    branch_revenue.save()
                
                logger.info(f"지점 {branch.name} 매출 업데이트 완료: {branch_revenue.total_revenue}원")
        
        logger.info("지점별 매출 업데이트 완료")
        return True
        
    except Exception as e:
        logger.error(f"지점별 매출 업데이트 중 오류 발생: {str(e)}")
        return False


def calculate_branch_pt_revenue(branch, year, month):
    """지점 PT 매출 계산"""
    pt_records = PTRecord.objects.filter(
        trainer__branch=branch,
        workout_date__year=year,
        workout_date__month=month,
        is_completed=True
    )
    
    total_revenue = Decimal('0')
    for pt_record in pt_records:
        if pt_record.reservation.pt_registration:
            pt_registration = pt_record.reservation.pt_registration
            session_price = pt_registration.total_price / pt_registration.total_sessions
            total_revenue += session_price
    
    return total_revenue


def calculate_branch_membership_revenue(branch, year, month):
    """지점 회원권 매출 계산"""
    # 실제 구현에서는 회원권 매출 데이터를 별도로 관리해야 함
    # 현재는 기본값 0으로 설정
    return Decimal('0')


def calculate_branch_additional_revenue(branch, year, month):
    """지점 추가 매출 계산"""
    # 실제 구현에서는 추가 매출 데이터를 별도로 관리해야 함
    # 현재는 기본값 0으로 설정
    return Decimal('0') 