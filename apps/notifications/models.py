from django.db import models
from apps.branches.models import BranchAdmin
from apps.members.models import Member
from apps.trainers.models import Trainer
from apps.reservations.models import Reservation


class Notification(models.Model):
    """알림 모델"""
    NOTIFICATION_TYPE_CHOICES = [
        ('reservation_request', '예약 요청'),
        ('reservation_confirmed', '예약 확정'),
        ('reservation_rejected', '예약 거절'),
        ('reservation_cancelled', '예약 취소'),
        ('reservation_reminder', '예약 알림'),
        ('pt_completed', 'PT 완료'),
        ('salary_paid', '급여 지급'),
        ('system', '시스템 알림'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '낮음'),
        ('medium', '보통'),
        ('high', '높음'),
        ('urgent', '긴급'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('sent', '전송완료'),
        ('failed', '전송실패'),
        ('read', '읽음'),
    ]
    
    notification_type = models.CharField(
        max_length=30, 
        choices=NOTIFICATION_TYPE_CHOICES, 
        verbose_name='알림 유형'
    )
    recipient_type = models.CharField(
        max_length=20, 
        verbose_name='수신자 유형'
    )
    recipient_id = models.PositiveIntegerField(verbose_name='수신자 ID')
    title = models.CharField(max_length=200, verbose_name='제목')
    message = models.TextField(verbose_name='메시지')
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium',
        verbose_name='우선순위'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='상태'
    )
    kakao_sent = models.BooleanField(default=False, verbose_name='카카오톡 전송')
    kakao_sent_at = models.DateTimeField(
        verbose_name='카카오톡 전송일시',
        null=True, 
        blank=True
    )
    read_at = models.DateTimeField(
        verbose_name='읽음 처리일시',
        null=True, 
        blank=True
    )
    related_reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.SET_NULL, 
        verbose_name='관련 예약',
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '알림'
        verbose_name_plural = '알림들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def get_recipient(self):
        """수신자 객체 반환"""
        if self.recipient_type == 'admin':
            return BranchAdmin.objects.filter(id=self.recipient_id).first()
        elif self.recipient_type == 'member':
            return Member.objects.filter(id=self.recipient_id).first()
        elif self.recipient_type == 'trainer':
            return Trainer.objects.filter(id=self.recipient_id).first()
        return None


class NotificationTemplate(models.Model):
    """알림 템플릿 모델"""
    NOTIFICATION_TYPE_CHOICES = [
        ('reservation_request', '예약 요청'),
        ('reservation_confirmed', '예약 확정'),
        ('reservation_rejected', '예약 거절'),
        ('reservation_cancelled', '예약 취소'),
        ('reservation_reminder', '예약 알림'),
        ('pt_completed', 'PT 완료'),
        ('salary_paid', '급여 지급'),
        ('system', '시스템 알림'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='템플릿명')
    notification_type = models.CharField(
        max_length=30, 
        choices=NOTIFICATION_TYPE_CHOICES, 
        verbose_name='알림 유형'
    )
    title_template = models.CharField(max_length=200, verbose_name='제목 템플릿')
    message_template = models.TextField(verbose_name='메시지 템플릿')
    kakao_template_id = models.CharField(
        max_length=100, 
        verbose_name='카카오톡 템플릿 ID',
        blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '알림 템플릿'
        verbose_name_plural = '알림 템플릿들'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_notification_type_display()})"


class NotificationLog(models.Model):
    """알림 전송 로그 모델"""
    LOG_TYPE_CHOICES = [
        ('kakao_success', '카카오톡 성공'),
        ('kakao_failed', '카카오톡 실패'),
        ('email_success', '이메일 성공'),
        ('email_failed', '이메일 실패'),
        ('sms_success', 'SMS 성공'),
        ('sms_failed', 'SMS 실패'),
    ]
    
    notification = models.ForeignKey(
        Notification, 
        on_delete=models.CASCADE, 
        verbose_name='알림',
        related_name='logs'
    )
    log_type = models.CharField(
        max_length=20, 
        choices=LOG_TYPE_CHOICES, 
        verbose_name='로그 유형'
    )
    recipient = models.CharField(max_length=100, verbose_name='수신자')
    message = models.TextField(verbose_name='전송 메시지')
    response = models.TextField(verbose_name='응답', blank=True)
    error_message = models.TextField(verbose_name='오류 메시지', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '알림 로그'
        verbose_name_plural = '알림 로그들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification} - {self.get_log_type_display()}"


class NotificationSetting(models.Model):
    """알림 설정 모델"""
    NOTIFICATION_CHANNEL_CHOICES = [
        ('kakao', '카카오톡'),
        ('email', '이메일'),
        ('sms', 'SMS'),
        ('push', '푸시 알림'),
    ]
    
    user_type = models.CharField(max_length=20, verbose_name='사용자 유형')
    user_id = models.PositiveIntegerField(verbose_name='사용자 ID')
    notification_type = models.CharField(
        max_length=30, 
        verbose_name='알림 유형'
    )
    channel = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_CHANNEL_CHOICES, 
        verbose_name='알림 채널'
    )
    is_enabled = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '알림 설정'
        verbose_name_plural = '알림 설정들'
        unique_together = ['user_type', 'user_id', 'notification_type', 'channel']
        ordering = ['user_type', 'user_id']

    def __str__(self):
        return f"{self.user_type}:{self.user_id} - {self.notification_type} ({self.channel})"

