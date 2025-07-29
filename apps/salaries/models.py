from django.db import models
from django.core.validators import MinValueValidator
from apps.trainers.models import Trainer
from apps.branches.models import Branch


class Salary(models.Model):
    """트레이너 급여 모델"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', '대기중'),
        ('paid', '지급완료'),
        ('cancelled', '취소'),
    ]
    
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        verbose_name='트레이너'
    )
    year = models.PositiveIntegerField(verbose_name='년도')
    month = models.PositiveIntegerField(
        verbose_name='월',
        validators=[MinValueValidator(1)]
    )
    base_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='기본급'
    )
    incentive_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='인센티브',
        default=0
    )
    additional_revenue = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='추가매출',
        default=0
    )
    other_costs = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='기타비용',
        default=0
    )
    total_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='총 급여'
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending',
        verbose_name='지급 상태'
    )
    payment_date = models.DateField(verbose_name='지급일', null=True, blank=True)
    notes = models.TextField(verbose_name='메모', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '급여'
        verbose_name_plural = '급여들'
        unique_together = ['trainer', 'year', 'month']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.trainer.name} - {self.year}년 {self.month}월"

    def calculate_total_salary(self):
        """총 급여 계산"""
        return self.base_salary + self.incentive_amount + self.additional_revenue - self.other_costs

    def save(self, *args, **kwargs):
        """저장 시 총 급여 자동 계산"""
        self.total_salary = self.calculate_total_salary()
        super().save(*args, **kwargs)


class IncentiveDetail(models.Model):
    """인센티브 상세 내역 모델"""
    INCENTIVE_TYPE_CHOICES = [
        ('pt_session', 'PT 세션'),
        ('new_member', '신규 회원'),
        ('retention', '회원 유지'),
        ('sales', '매출'),
        ('other', '기타'),
    ]
    
    salary = models.ForeignKey(
        Salary, 
        on_delete=models.CASCADE, 
        verbose_name='급여',
        related_name='incentive_details'
    )
    incentive_type = models.CharField(
        max_length=20, 
        choices=INCENTIVE_TYPE_CHOICES, 
        verbose_name='인센티브 유형'
    )
    quantity = models.PositiveIntegerField(verbose_name='수량')
    unit_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='단가'
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='총 금액'
    )
    description = models.TextField(verbose_name='설명', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '인센티브 상세'
        verbose_name_plural = '인센티브 상세들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.salary} - {self.get_incentive_type_display()}"


class AdditionalRevenue(models.Model):
    """추가매출 모델"""
    REVENUE_TYPE_CHOICES = [
        ('supplement_sales', '보충제 판매'),
        ('equipment_sales', '운동용품 판매'),
        ('consultation', '상담료'),
        ('other', '기타'),
    ]
    
    salary = models.ForeignKey(
        Salary, 
        on_delete=models.CASCADE, 
        verbose_name='급여',
        related_name='additional_revenues'
    )
    revenue_type = models.CharField(
        max_length=20, 
        choices=REVENUE_TYPE_CHOICES, 
        verbose_name='매출 유형'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='금액'
    )
    description = models.TextField(verbose_name='설명', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '추가매출'
        verbose_name_plural = '추가매출들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.salary} - {self.get_revenue_type_display()}"


class OtherCost(models.Model):
    """기타비용 모델"""
    COST_TYPE_CHOICES = [
        ('insurance', '보험료'),
        ('tax', '세금'),
        ('deduction', '공제'),
        ('penalty', '벌금'),
        ('other', '기타'),
    ]
    
    salary = models.ForeignKey(
        Salary, 
        on_delete=models.CASCADE, 
        verbose_name='급여',
        related_name='other_cost_items'
    )
    cost_type = models.CharField(
        max_length=20, 
        choices=COST_TYPE_CHOICES, 
        verbose_name='비용 유형'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='금액'
    )
    description = models.TextField(verbose_name='설명', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '기타비용'
        verbose_name_plural = '기타비용들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.salary} - {self.get_cost_type_display()}"


class BranchRevenue(models.Model):
    """지점별 매출 모델"""
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        verbose_name='지점'
    )
    year = models.PositiveIntegerField(verbose_name='년도')
    month = models.PositiveIntegerField(
        verbose_name='월',
        validators=[MinValueValidator(1)]
    )
    pt_revenue = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name='PT 매출',
        default=0
    )
    membership_revenue = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name='회원권 매출',
        default=0
    )
    additional_revenue = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name='추가 매출',
        default=0
    )
    total_revenue = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name='총 매출'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '지점 매출'
        verbose_name_plural = '지점 매출들'
        unique_together = ['branch', 'year', 'month']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.branch.name} - {self.year}년 {self.month}월"

    def calculate_total_revenue(self):
        """총 매출 계산"""
        return self.pt_revenue + self.membership_revenue + self.additional_revenue

    def save(self, *args, **kwargs):
        """저장 시 총 매출 자동 계산"""
        self.total_revenue = self.calculate_total_revenue()
        super().save(*args, **kwargs)

