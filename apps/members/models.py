from django.db import models
from django.core.validators import RegexValidator
from apps.branches.models import Branch


class Member(models.Model):
    """회원 모델"""
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    MEMBERSHIP_STATUS_CHOICES = [
        ('active', '활성'),
        ('inactive', '비활성'),
        ('suspended', '정지'),
        ('expired', '만료'),
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
    membership_status = models.CharField(
        max_length=20, 
        choices=MEMBERSHIP_STATUS_CHOICES, 
        default='active',
        verbose_name='회원 상태'
    )
    registration_date = models.DateField(auto_now_add=True, verbose_name='가입일')
    expiry_date = models.DateField(verbose_name='만료일', null=True, blank=True)
    notes = models.TextField(verbose_name='메모', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.branch.name})"


class PTProgram(models.Model):
    """PT 프로그램 모델"""
    PROGRAM_TYPE_CHOICES = [
        ('new', '신규'),
        ('long_term', '장기'),
        ('short_term', '단기'),
    ]
    
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        verbose_name='소속 지점'
    )
    name = models.CharField(max_length=100, verbose_name='프로그램명')
    program_type = models.CharField(
        max_length=20, 
        choices=PROGRAM_TYPE_CHOICES, 
        verbose_name='프로그램 유형'
    )
    sessions = models.PositiveIntegerField(verbose_name='PT 횟수')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='가격'
    )
    description = models.TextField(verbose_name='설명', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = 'PT 프로그램'
        verbose_name_plural = 'PT 프로그램들'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_program_type_display()})"


class MemberPTRegistration(models.Model):
    """회원 PT 등록 모델"""
    REGISTRATION_STATUS_CHOICES = [
        ('active', '활성'),
        ('completed', '완료'),
        ('cancelled', '취소'),
        ('expired', '만료'),
    ]
    
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE, 
        verbose_name='회원'
    )
    pt_program = models.ForeignKey(
        PTProgram, 
        on_delete=models.CASCADE, 
        verbose_name='PT 프로그램'
    )
    trainer = models.ForeignKey(
        'trainers.Trainer', 
        on_delete=models.CASCADE, 
        verbose_name='담당 트레이너',
        null=True, 
        blank=True
    )
    total_sessions = models.PositiveIntegerField(verbose_name='총 PT 횟수')
    remaining_sessions = models.PositiveIntegerField(verbose_name='남은 PT 횟수')
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='총 가격'
    )
    paid_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='결제 금액',
        default=0
    )
    registration_status = models.CharField(
        max_length=20, 
        choices=REGISTRATION_STATUS_CHOICES, 
        default='active',
        verbose_name='등록 상태'
    )
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    expiry_date = models.DateField(verbose_name='만료일', null=True, blank=True)
    notes = models.TextField(verbose_name='메모', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '회원 PT 등록'
        verbose_name_plural = '회원 PT 등록들'
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.member.name} - {self.pt_program.name}"

    def get_completion_rate(self):
        """완료율 계산"""
        if self.total_sessions == 0:
            return 0
        completed = self.total_sessions - self.remaining_sessions
        return (completed / self.total_sessions) * 100

