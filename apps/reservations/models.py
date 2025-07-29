from django.db import models
from django.core.validators import MinValueValidator
from model_utils import FieldTracker
from apps.members.models import Member, MemberPTRegistration
from apps.trainers.models import Trainer


class Reservation(models.Model):
    """PT 예약 모델"""
    RESERVATION_STATUS_CHOICES = [
        ('pending', '대기중'),
        ('confirmed', '확정'),
        ('rejected', '거절'),
        ('cancelled', '취소'),
        ('completed', '완료'),
        ('no_show', '노쇼'),
    ]
    
    REPEAT_TYPE_CHOICES = [
        ('none', '반복 없음'),
        ('daily', '매일'),
        ('weekly', '매주'),
        ('monthly', '매월'),
    ]
    
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE, 
        verbose_name='회원'
    )
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        verbose_name='트레이너'
    )
    pt_registration = models.ForeignKey(
        MemberPTRegistration, 
        on_delete=models.CASCADE, 
        verbose_name='PT 등록',
        null=True, 
        blank=True
    )
    date = models.DateField(verbose_name='예약 날짜')
    start_time = models.TimeField(verbose_name='시작 시간')
    end_time = models.TimeField(verbose_name='종료 시간')
    duration = models.PositiveIntegerField(
        verbose_name='PT 시간 (분)',
        default=30,
        validators=[MinValueValidator(30)]
    )
    reservation_status = models.CharField(
        max_length=20, 
        choices=RESERVATION_STATUS_CHOICES, 
        default='pending',
        verbose_name='예약 상태'
    )
    repeat_type = models.CharField(
        max_length=20, 
        choices=REPEAT_TYPE_CHOICES, 
        default='none',
        verbose_name='반복 유형'
    )
    repeat_end_date = models.DateField(
        verbose_name='반복 종료일',
        null=True, 
        blank=True
    )
    notes = models.TextField(verbose_name='메모', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = 'PT 예약'
        verbose_name_plural = 'PT 예약들'
        ordering = ['-date', '-start_time']
        unique_together = ['trainer', 'date', 'start_time']

    def __str__(self):
        return f"{self.member.name} - {self.trainer.name} ({self.date} {self.start_time})"

    def get_duration_display(self):
        """PT 시간 표시"""
        return f"{self.duration}분"
    
    # 필드 변경 추적
    tracker = FieldTracker(fields=['reservation_status'])


class PTRecord(models.Model):
    """PT 수행 내역 모델"""
    reservation = models.OneToOneField(
        Reservation, 
        on_delete=models.CASCADE, 
        verbose_name='예약'
    )
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
        verbose_name='트레이너'
    )
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE, 
        verbose_name='회원'
    )
    workout_date = models.DateField(verbose_name='운동 날짜')
    workout_time = models.TimeField(verbose_name='운동 시간')
    duration = models.PositiveIntegerField(verbose_name='실제 운동 시간 (분)')
    content = models.TextField(verbose_name='운동 내용')
    member_condition = models.TextField(verbose_name='회원 상태', blank=True)
    trainer_notes = models.TextField(verbose_name='트레이너 메모', blank=True)
    is_completed = models.BooleanField(default=False, verbose_name='완료 여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = 'PT 수행 내역'
        verbose_name_plural = 'PT 수행 내역들'
        ordering = ['-workout_date', '-workout_time']

    def __str__(self):
        return f"{self.member.name} - {self.trainer.name} ({self.workout_date})"
    
    # 필드 변경 추적
    tracker = FieldTracker(fields=['is_completed'])


class PTRecordImage(models.Model):
    """PT 수행 내역 이미지 모델"""
    pt_record = models.ForeignKey(
        PTRecord, 
        on_delete=models.CASCADE, 
        verbose_name='PT 수행 내역',
        related_name='images'
    )
    image = models.ImageField(
        upload_to='pt_records/images/', 
        verbose_name='이미지'
    )
    description = models.CharField(
        max_length=200, 
        verbose_name='설명',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = 'PT 수행 내역 이미지'
        verbose_name_plural = 'PT 수행 내역 이미지들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pt_record} - {self.description or '이미지'}"


class ReservationChangeLog(models.Model):
    """예약 변경 로그 모델"""
    CHANGE_TYPE_CHOICES = [
        ('created', '생성'),
        ('confirmed', '확정'),
        ('rejected', '거절'),
        ('cancelled', '취소'),
        ('modified', '수정'),
        ('completed', '완료'),
    ]
    
    reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.CASCADE, 
        verbose_name='예약',
        related_name='change_logs'
    )
    change_type = models.CharField(
        max_length=20, 
        choices=CHANGE_TYPE_CHOICES, 
        verbose_name='변경 유형'
    )
    changed_by = models.CharField(max_length=100, verbose_name='변경자')
    previous_status = models.CharField(
        max_length=20, 
        verbose_name='이전 상태',
        blank=True
    )
    new_status = models.CharField(
        max_length=20, 
        verbose_name='새로운 상태',
        blank=True
    )
    reason = models.TextField(verbose_name='변경 사유', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '예약 변경 로그'
        verbose_name_plural = '예약 변경 로그들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reservation} - {self.get_change_type_display()}"

