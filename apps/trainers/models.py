from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from apps.branches.models import Branch


class Trainer(models.Model):
    """트레이너 모델"""
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    EMPLOYMENT_STATUS_CHOICES = [
        ('active', '재직'),
        ('inactive', '휴직'),
        ('resigned', '퇴사'),
    ]
    
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        verbose_name='소속 지점'
    )
    name = models.CharField(max_length=100, verbose_name='이름')
    phone = models.CharField(
        max_length=20, 
        verbose_name='전화번호',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="전화번호는 '+999999999' 형식으로 입력해주세요."
            )
        ]
    )
    email = models.EmailField(verbose_name='이메일', blank=True)
    birth_date = models.DateField(verbose_name='생년월일', null=True, blank=True)
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        verbose_name='성별',
        null=True, 
        blank=True
    )
    address = models.TextField(verbose_name='주소', blank=True)
    emergency_contact = models.CharField(
        max_length=20, 
        verbose_name='비상연락처',
        blank=True
    )
    employment_status = models.CharField(
        max_length=20, 
        choices=EMPLOYMENT_STATUS_CHOICES, 
        default='active',
        verbose_name='재직 상태'
    )
    hire_date = models.DateField(verbose_name='입사일')
    base_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='기본급'
    )
    kakao_id = models.CharField(
        max_length=100, 
        verbose_name='카카오톡 ID',
        blank=True
    )
    profile_image = models.ImageField(
        upload_to='trainers/profiles/', 
        verbose_name='프로필 이미지',
        null=True, 
        blank=True
    )
    specialties = models.TextField(verbose_name='전문 분야', blank=True)
    certifications = models.TextField(verbose_name='자격증', blank=True)
    experience_years = models.PositiveIntegerField(
        verbose_name='경력 연차',
        default=0
    )
    notes = models.TextField(verbose_name='메모', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '트레이너'
        verbose_name_plural = '트레이너들'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.branch.name})"


class TrainerIncentive(models.Model):
    """트레이너 인센티브 설정 모델"""
    INCENTIVE_TYPE_CHOICES = [
        ('fixed', '고정 금액'),
        ('percentage', '퍼센티지'),
    ]
    
    trainer = models.OneToOneField(
        Trainer, 
        on_delete=models.CASCADE, 
        verbose_name='트레이너'
    )
    incentive_type = models.CharField(
        max_length=20, 
        choices=INCENTIVE_TYPE_CHOICES, 
        default='fixed',
        verbose_name='인센티브 유형'
    )
    fixed_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='고정 금액',
        default=0
    )
    percentage_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name='퍼센티지 비율 (%)',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '트레이너 인센티브'
        verbose_name_plural = '트레이너 인센티브들'

    def __str__(self):
        if self.incentive_type == 'fixed':
            return f"{self.trainer.name} - {self.fixed_amount}원"
        return f"{self.trainer.name} - {self.percentage_rate}%"


class TrainerSchedule(models.Model):
    """트레이너 일정 모델"""
    DAY_OF_WEEK_CHOICES = [
        (0, '월요일'),
        (1, '화요일'),
        (2, '수요일'),
        (3, '목요일'),
        (4, '금요일'),
        (5, '토요일'),
        (6, '일요일'),
    ]
    
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        verbose_name='트레이너'
    )
    day_of_week = models.IntegerField(
        choices=DAY_OF_WEEK_CHOICES, 
        verbose_name='요일'
    )
    start_time = models.TimeField(verbose_name='시작 시간')
    end_time = models.TimeField(verbose_name='종료 시간')
    is_available = models.BooleanField(default=True, verbose_name='근무 가능')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '트레이너 일정'
        verbose_name_plural = '트레이너 일정들'
        unique_together = ['trainer', 'day_of_week']
        ordering = ['trainer', 'day_of_week']

    def __str__(self):
        return f"{self.trainer.name} - {self.get_day_of_week_display()}"


class TrainerBlockedTime(models.Model):
    """트레이너 차단 시간 모델"""
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        verbose_name='트레이너'
    )
    date = models.DateField(verbose_name='날짜')
    start_time = models.TimeField(verbose_name='시작 시간')
    end_time = models.TimeField(verbose_name='종료 시간')
    reason = models.CharField(max_length=200, verbose_name='차단 사유', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '트레이너 차단 시간'
        verbose_name_plural = '트레이너 차단 시간들'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.trainer.name} - {self.date} {self.start_time}-{self.end_time}"

