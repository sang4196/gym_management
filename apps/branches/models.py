from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Branch(models.Model):
    """헬스장 지점 모델"""
    name = models.CharField(max_length=100, verbose_name='지점명')
    address = models.TextField(verbose_name='주소')
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
    email = models.EmailField(verbose_name='이메일')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '지점'
        verbose_name_plural = '지점들'
        ordering = ['name']

    def __str__(self):
        return self.name


class BranchAdmin(AbstractUser):
    """지점별 어드민 모델"""
    ADMIN_TYPE_CHOICES = [
        ('headquarters', '본사'),
        ('branch', '지점'),
    ]
    
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        verbose_name='소속 지점',
        null=True, 
        blank=True
    )
    admin_type = models.CharField(
        max_length=20, 
        choices=ADMIN_TYPE_CHOICES, 
        default='branch',
        verbose_name='어드민 유형'
    )
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
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '어드민'
        verbose_name_plural = '어드민들'
        ordering = ['username']

    def __str__(self):
        if self.admin_type == 'headquarters':
            return f"{self.username} (본사)"
        return f"{self.username} ({self.branch.name if self.branch else '지점미지정'})"

    def get_branch_name(self):
        """지점명 반환"""
        if self.admin_type == 'headquarters':
            return '본사'
        return self.branch.name if self.branch else '지점미지정'

