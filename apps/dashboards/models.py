from django.db import models
from apps.branches.models import Branch


class DashboardWidget(models.Model):
    """대시보드 위젯 모델"""
    WIDGET_TYPE_CHOICES = [
        ('revenue_chart', '매출 차트'),
        ('member_stats', '회원 통계'),
        ('trainer_stats', '트레이너 통계'),
        ('reservation_stats', '예약 통계'),
        ('salary_stats', '급여 통계'),
        ('custom_chart', '커스텀 차트'),
        ('data_table', '데이터 테이블'),
        ('metric_card', '메트릭 카드'),
    ]
    
    CHART_TYPE_CHOICES = [
        ('line', '선 그래프'),
        ('bar', '막대 그래프'),
        ('pie', '파이 차트'),
        ('doughnut', '도넛 차트'),
        ('area', '영역 그래프'),
        ('scatter', '산점도'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='위젯명')
    widget_type = models.CharField(
        max_length=20, 
        choices=WIDGET_TYPE_CHOICES, 
        verbose_name='위젯 유형'
    )
    chart_type = models.CharField(
        max_length=20, 
        choices=CHART_TYPE_CHOICES, 
        verbose_name='차트 유형',
        blank=True
    )
    title = models.CharField(max_length=200, verbose_name='제목')
    description = models.TextField(verbose_name='설명', blank=True)
    data_source = models.CharField(max_length=100, verbose_name='데이터 소스')
    config = models.JSONField(verbose_name='설정', default=dict)
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    sort_order = models.PositiveIntegerField(verbose_name='정렬 순서', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '대시보드 위젯'
        verbose_name_plural = '대시보드 위젯들'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"


class DashboardLayout(models.Model):
    """대시보드 레이아웃 모델"""
    LAYOUT_TYPE_CHOICES = [
        ('grid', '그리드'),
        ('flexible', '유연한 레이아웃'),
        ('custom', '커스텀'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='레이아웃명')
    layout_type = models.CharField(
        max_length=20, 
        choices=LAYOUT_TYPE_CHOICES, 
        default='grid',
        verbose_name='레이아웃 유형'
    )
    description = models.TextField(verbose_name='설명', blank=True)
    config = models.JSONField(verbose_name='설정', default=dict)
    is_default = models.BooleanField(default=False, verbose_name='기본 레이아웃')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '대시보드 레이아웃'
        verbose_name_plural = '대시보드 레이아웃들'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserDashboard(models.Model):
    """사용자별 대시보드 모델"""
    user_type = models.CharField(max_length=20, verbose_name='사용자 유형')
    user_id = models.PositiveIntegerField(verbose_name='사용자 ID')
    layout = models.ForeignKey(
        DashboardLayout, 
        on_delete=models.CASCADE, 
        verbose_name='레이아웃'
    )
    widgets = models.ManyToManyField(
        DashboardWidget, 
        through='UserDashboardWidget',
        verbose_name='위젯들'
    )
    config = models.JSONField(verbose_name='설정', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '사용자 대시보드'
        verbose_name_plural = '사용자 대시보드들'
        unique_together = ['user_type', 'user_id']
        ordering = ['user_type', 'user_id']

    def __str__(self):
        return f"{self.user_type}:{self.user_id}"


class UserDashboardWidget(models.Model):
    """사용자 대시보드 위젯 연결 모델"""
    user_dashboard = models.ForeignKey(
        UserDashboard, 
        on_delete=models.CASCADE, 
        verbose_name='사용자 대시보드'
    )
    widget = models.ForeignKey(
        DashboardWidget, 
        on_delete=models.CASCADE, 
        verbose_name='위젯'
    )
    position_x = models.PositiveIntegerField(verbose_name='X 위치')
    position_y = models.PositiveIntegerField(verbose_name='Y 위치')
    width = models.PositiveIntegerField(verbose_name='너비')
    height = models.PositiveIntegerField(verbose_name='높이')
    is_visible = models.BooleanField(default=True, verbose_name='표시 여부')
    config = models.JSONField(verbose_name='위젯 설정', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '사용자 대시보드 위젯'
        verbose_name_plural = '사용자 대시보드 위젯들'
        unique_together = ['user_dashboard', 'widget']
        ordering = ['position_y', 'position_x']

    def __str__(self):
        return f"{self.user_dashboard} - {self.widget.name}"


class Report(models.Model):
    """리포트 모델"""
    REPORT_TYPE_CHOICES = [
        ('revenue', '매출 리포트'),
        ('member', '회원 리포트'),
        ('trainer', '트레이너 리포트'),
        ('reservation', '예약 리포트'),
        ('salary', '급여 리포트'),
        ('custom', '커스텀 리포트'),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='리포트명')
    report_type = models.CharField(
        max_length=20, 
        choices=REPORT_TYPE_CHOICES, 
        verbose_name='리포트 유형'
    )
    description = models.TextField(verbose_name='설명', blank=True)
    query = models.TextField(verbose_name='쿼리')
    parameters = models.JSONField(verbose_name='매개변수', default=dict)
    format = models.CharField(
        max_length=10, 
        choices=FORMAT_CHOICES, 
        default='pdf',
        verbose_name='출력 형식'
    )
    schedule = models.CharField(max_length=100, verbose_name='스케줄', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '리포트'
        verbose_name_plural = '리포트들'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"


class ReportExecution(models.Model):
    """리포트 실행 로그 모델"""
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('running', '실행중'),
        ('completed', '완료'),
        ('failed', '실패'),
        ('cancelled', '취소'),
    ]
    
    report = models.ForeignKey(
        Report, 
        on_delete=models.CASCADE, 
        verbose_name='리포트'
    )
    executed_by = models.CharField(max_length=100, verbose_name='실행자')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='상태'
    )
    parameters = models.JSONField(verbose_name='실행 매개변수', default=dict)
    result_file = models.FileField(
        upload_to='reports/', 
        verbose_name='결과 파일',
        null=True, 
        blank=True
    )
    error_message = models.TextField(verbose_name='오류 메시지', blank=True)
    started_at = models.DateTimeField(verbose_name='시작일시', null=True, blank=True)
    completed_at = models.DateTimeField(verbose_name='완료일시', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '리포트 실행'
        verbose_name_plural = '리포트 실행들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.report.name} - {self.get_status_display()}"

