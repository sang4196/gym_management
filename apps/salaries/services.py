from decimal import Decimal
from datetime import datetime, date
from typing import Dict, List, Optional
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum, Count, Q
from .models import (
    Salary, IncentiveDetail, AdditionalRevenue, OtherCost,
    BranchRevenue
)
from apps.trainers.models import Trainer, TrainerIncentive
from apps.reservations.models import Reservation, PTRecord
from apps.members.models import MemberPTRegistration


class SalaryCalculationService:
    """급여 계산 서비스"""
    
    def __init__(self):
        pass
    
    def calculate_monthly_salary(
        self, 
        trainer: Trainer, 
        year: int, 
        month: int,
        force_recalculate: bool = False
    ) -> Salary:
        """월별 급여 계산"""
        
        # 기존 급여 확인
        existing_salary = Salary.objects.filter(
            trainer=trainer,
            year=year,
            month=month
        ).first()
        
        if existing_salary and not force_recalculate:
            return existing_salary
        
        with transaction.atomic():
            # 기본급
            base_salary = trainer.base_salary
            
            # 인센티브 계산
            incentive_amount = self._calculate_incentive(trainer, year, month)
            
            # 추가매출 계산
            additional_revenue = self._calculate_additional_revenue(trainer, year, month)
            
            # 기타비용 계산
            other_costs = self._calculate_other_costs(trainer, year, month)
            
            # 총 급여 계산
            total_salary = base_salary + incentive_amount + additional_revenue - other_costs
            
            # 급여 객체 생성 또는 업데이트
            if existing_salary:
                existing_salary.base_salary = base_salary
                existing_salary.incentive_amount = incentive_amount
                existing_salary.additional_revenue = additional_revenue
                existing_salary.other_costs = other_costs
                existing_salary.total_salary = total_salary
                existing_salary.save()
                salary = existing_salary
            else:
                salary = Salary.objects.create(
                    trainer=trainer,
                    year=year,
                    month=month,
                    base_salary=base_salary,
                    incentive_amount=incentive_amount,
                    additional_revenue=additional_revenue,
                    other_costs=other_costs,
                    total_salary=total_salary
                )
            
            # 상세 내역 생성
            self._create_incentive_details(salary, trainer, year, month)
            self._create_additional_revenue_details(salary, trainer, year, month)
            self._create_other_cost_details(salary, trainer, year, month)
            
            return salary
    
    def _calculate_incentive(self, trainer: Trainer, year: int, month: int) -> Decimal:
        """인센티브 계산"""
        try:
            incentive_config = TrainerIncentive.objects.get(trainer=trainer, is_active=True)
        except TrainerIncentive.DoesNotExist:
            return Decimal('0')
        
        total_incentive = Decimal('0')
        
        # PT 세션 인센티브
        pt_sessions = self._get_completed_pt_sessions(trainer, year, month)
        if incentive_config.incentive_type == 'fixed':
            total_incentive += pt_sessions * incentive_config.fixed_amount
        else:  # percentage
            # PT 세션당 평균 가격 계산
            avg_pt_price = self._get_average_pt_price(trainer, year, month)
            total_incentive += (pt_sessions * avg_pt_price * incentive_config.percentage_rate / 100)
        
        return total_incentive
    
    def _calculate_additional_revenue(self, trainer: Trainer, year: int, month: int) -> Decimal:
        """추가매출 계산"""
        # 보충제 판매, 운동용품 판매, 상담료 등
        # 실제 구현에서는 별도 모델에서 데이터를 가져와야 함
        return Decimal('0')
    
    def _calculate_other_costs(self, trainer: Trainer, year: int, month: int) -> Decimal:
        """기타비용 계산"""
        # 보험료, 세금, 공제, 벌금 등
        # 실제 구현에서는 별도 모델에서 데이터를 가져와야 함
        return Decimal('0')
    
    def _get_completed_pt_sessions(self, trainer: Trainer, year: int, month: int) -> int:
        """완료된 PT 세션 수 조회"""
        return PTRecord.objects.filter(
            trainer=trainer,
            workout_date__year=year,
            workout_date__month=month,
            is_completed=True
        ).count()
    
    def _get_average_pt_price(self, trainer: Trainer, year: int, month: int) -> Decimal:
        """PT 세션당 평균 가격 계산"""
        pt_registrations = MemberPTRegistration.objects.filter(
            trainer=trainer,
            registration_date__year=year,
            registration_date__month=month
        )
        
        if not pt_registrations.exists():
            return Decimal('50000')  # 기본값
        
        total_price = pt_registrations.aggregate(
            total=Sum('total_price')
        )['total'] or Decimal('0')
        
        total_sessions = pt_registrations.aggregate(
            total=Sum('total_sessions')
        )['total'] or 0
        
        if total_sessions == 0:
            return Decimal('50000')
        
        return total_price / total_sessions
    
    def _create_incentive_details(self, salary: Salary, trainer: Trainer, year: int, month: int):
        """인센티브 상세 내역 생성"""
        # 기존 상세 내역 삭제
        IncentiveDetail.objects.filter(salary=salary).delete()
        
        # PT 세션 인센티브
        pt_sessions = self._get_completed_pt_sessions(trainer, year, month)
        if pt_sessions > 0:
            try:
                incentive_config = TrainerIncentive.objects.get(trainer=trainer, is_active=True)
                if incentive_config.incentive_type == 'fixed':
                    unit_amount = incentive_config.fixed_amount
                else:
                    avg_price = self._get_average_pt_price(trainer, year, month)
                    unit_amount = avg_price * incentive_config.percentage_rate / 100
                
                IncentiveDetail.objects.create(
                    salary=salary,
                    incentive_type='pt_session',
                    quantity=pt_sessions,
                    unit_amount=unit_amount,
                    total_amount=pt_sessions * unit_amount,
                    description=f"{year}년 {month}월 PT 세션 {pt_sessions}회"
                )
            except TrainerIncentive.DoesNotExist:
                pass
    
    def _create_additional_revenue_details(self, salary: Salary, trainer: Trainer, year: int, month: int):
        """추가매출 상세 내역 생성"""
        # 기존 상세 내역 삭제
        AdditionalRevenue.objects.filter(salary=salary).delete()
        
        # 실제 구현에서는 추가매출 데이터를 가져와서 상세 내역 생성
        pass
    
    def _create_other_cost_details(self, salary: Salary, trainer: Trainer, year: int, month: int):
        """기타비용 상세 내역 생성"""
        # 기존 상세 내역 삭제
        OtherCost.objects.filter(salary=salary).delete()
        
        # 실제 구현에서는 기타비용 데이터를 가져와서 상세 내역 생성
        pass
    
    def calculate_all_trainers_salary(self, year: int, month: int) -> List[Salary]:
        """모든 트레이너의 급여 계산"""
        salaries = []
        trainers = Trainer.objects.filter(employment_status='active')
        
        for trainer in trainers:
            salary = self.calculate_monthly_salary(trainer, year, month)
            salaries.append(salary)
        
        return salaries
    
    def get_salary_summary(self, year: int, month: int, branch_id: Optional[int] = None) -> Dict:
        """급여 요약 정보"""
        queryset = Salary.objects.filter(year=year, month=month)
        
        if branch_id:
            queryset = queryset.filter(trainer__branch_id=branch_id)
        
        summary = queryset.aggregate(
            total_trainers=Count('id'),
            total_base_salary=Sum('base_salary'),
            total_incentive=Sum('incentive_amount'),
            total_additional_revenue=Sum('additional_revenue'),
            total_other_costs=Sum('other_costs'),
            total_salary=Sum('total_salary')
        )
        
        return summary


class BranchRevenueService:
    """지점 매출 계산 서비스"""
    
    def __init__(self):
        pass
    
    def calculate_monthly_revenue(
        self, 
        branch_id: int, 
        year: int, 
        month: int,
        force_recalculate: bool = False
    ) -> BranchRevenue:
        """월별 지점 매출 계산"""
        
        # 기존 매출 확인
        existing_revenue = BranchRevenue.objects.filter(
            branch_id=branch_id,
            year=year,
            month=month
        ).first()
        
        if existing_revenue and not force_recalculate:
            return existing_revenue
        
        # PT 매출 계산
        pt_revenue = self._calculate_pt_revenue(branch_id, year, month)
        
        # 회원권 매출 계산
        membership_revenue = self._calculate_membership_revenue(branch_id, year, month)
        
        # 추가 매출 계산
        additional_revenue = self._calculate_branch_additional_revenue(branch_id, year, month)
        
        # 총 매출 계산
        total_revenue = pt_revenue + membership_revenue + additional_revenue
        
        # 매출 객체 생성 또는 업데이트
        if existing_revenue:
            existing_revenue.pt_revenue = pt_revenue
            existing_revenue.membership_revenue = membership_revenue
            existing_revenue.additional_revenue = additional_revenue
            existing_revenue.total_revenue = total_revenue
            existing_revenue.save()
            return existing_revenue
        else:
            return BranchRevenue.objects.create(
                branch_id=branch_id,
                year=year,
                month=month,
                pt_revenue=pt_revenue,
                membership_revenue=membership_revenue,
                additional_revenue=additional_revenue,
                total_revenue=total_revenue
            )
    
    def _calculate_pt_revenue(self, branch_id: int, year: int, month: int) -> Decimal:
        """PT 매출 계산"""
        return MemberPTRegistration.objects.filter(
            member__branch_id=branch_id,
            registration_date__year=year,
            registration_date__month=month
        ).aggregate(
            total=Sum('total_price')
        )['total'] or Decimal('0')
    
    def _calculate_membership_revenue(self, branch_id: int, year: int, month: int) -> Decimal:
        """회원권 매출 계산"""
        # 실제 구현에서는 회원권 등록/갱신 데이터를 가져와서 계산
        return Decimal('0')
    
    def _calculate_branch_additional_revenue(self, branch_id: int, year: int, month: int) -> Decimal:
        """지점 추가 매출 계산"""
        # 보충제 판매, 운동용품 판매 등
        return Decimal('0')
    
    def calculate_all_branches_revenue(self, year: int, month: int) -> List[BranchRevenue]:
        """모든 지점의 매출 계산"""
        from apps.branches.models import Branch
        
        revenues = []
        branches = Branch.objects.filter(is_active=True)
        
        for branch in branches:
            revenue = self.calculate_monthly_revenue(branch.id, year, month)
            revenues.append(revenue)
        
        return revenues


# 싱글톤 인스턴스
salary_calculation_service = SalaryCalculationService()
branch_revenue_service = BranchRevenueService() 