from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg
from datetime import date, timedelta
from .models import (
    DashboardWidget, DashboardLayout, UserDashboard, 
    UserDashboardWidget, Report, ReportExecution
)
from .serializers import (
    DashboardWidgetSerializer,
    DashboardLayoutSerializer,
    UserDashboardSerializer,
    UserDashboardWidgetSerializer,
    ReportSerializer,
    ReportExecutionSerializer,
    UserDashboardDetailSerializer,
    ReportDetailSerializer
)
from .permissions import (
    DashboardWidgetPermission,
    DashboardLayoutPermission,
    UserDashboardPermission,
    UserDashboardWidgetPermission,
    ReportPermission,
    ReportExecutionPermission
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from apps.branches.models import Branch
from apps.members.models import Member, MemberPTRegistration
from apps.trainers.models import Trainer
from apps.reservations.models import Reservation, PTRecord
from apps.salaries.models import Salary, BranchRevenue
from apps.notifications.models import Notification


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    """대시보드 위젯 API 뷰셋"""
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [DashboardWidgetPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['widget_type', 'chart_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """사용 가능한 위젯 목록"""
        available_widgets = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(available_widgets, many=True)
        return Response(serializer.data)

class DashboardLayoutViewSet(viewsets.ModelViewSet):
    """대시보드 레이아웃 API 뷰셋"""
    queryset = DashboardLayout.objects.all()
    serializer_class = DashboardLayoutSerializer
    permission_classes = [DashboardLayoutPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['layout_type', 'is_default']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class UserDashboardViewSet(viewsets.ModelViewSet):
    """사용자 대시보드 API 뷰셋"""
    queryset = UserDashboard.objects.all()
    serializer_class = UserDashboardSerializer
    permission_classes = [UserDashboardPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'is_default']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return UserDashboard.objects.all()
        else:
            return UserDashboard.objects.filter(user=user)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return UserDashboardDetailSerializer
        return UserDashboardSerializer
    
    @action(detail=False, methods=['get'])
    def my_dashboards(self, request):
        """내 대시보드 목록"""
        my_dashboards = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(my_dashboards, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """기본 대시보드 설정"""
        dashboard = self.get_object()
        
        # 기존 기본 대시보드 해제
        UserDashboard.objects.filter(user=request.user, is_default=True).update(is_default=False)
        
        # 새로운 기본 대시보드 설정
        dashboard.is_default = True
        dashboard.save()
        
        return Response({'message': '기본 대시보드가 설정되었습니다.'})

class UserDashboardWidgetViewSet(viewsets.ModelViewSet):
    """사용자 대시보드 위젯 API 뷰셋"""
    queryset = UserDashboardWidget.objects.all()
    serializer_class = UserDashboardWidgetSerializer
    permission_classes = [UserDashboardWidgetPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['dashboard', 'widget']
    search_fields = ['widget__name']
    ordering_fields = ['position', 'created_at']
    ordering = ['dashboard__name', 'position']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return UserDashboardWidget.objects.all()
        else:
            return UserDashboardWidget.objects.filter(dashboard__user=user)

class ReportViewSet(viewsets.ModelViewSet):
    """리포트 API 뷰셋"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [ReportPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return ReportDetailSerializer
        return ReportSerializer
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """리포트 실행"""
        report = self.get_object()
        
        # 리포트 실행 기록
        execution = ReportExecution.objects.create(
            report=report,
            executed_by=request.user,
            status='running',
            parameters=request.data.get('parameters', {})
        )
        
        # 실제 리포트 실행 로직은 여기에 구현
        # 예: 데이터 수집, 파일 생성 등
        
        execution.status = 'completed'
        execution.save()
        
        return Response({
            'message': '리포트가 실행되었습니다.',
            'execution_id': execution.id
        })

class ReportExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    """리포트 실행 API 뷰셋 (읽기 전용)"""
    queryset = ReportExecution.objects.all()
    serializer_class = ReportExecutionSerializer
    permission_classes = [ReportExecutionPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report', 'status', 'executed_by']
    search_fields = ['report__name']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return ReportExecution.objects.all()
        else:
            return ReportExecution.objects.filter(executed_by=user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """최근 실행 기록"""
        recent_executions = self.get_queryset().order_by('-created_at')[:20]
        serializer = self.get_serializer(recent_executions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def failed(self, request):
        """실패한 실행 기록"""
        failed_executions = self.get_queryset().filter(status='failed').order_by('-created_at')
        serializer = self.get_serializer(failed_executions, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """대시보드 개요 통계"""
    user = request.user
    branch_id = request.GET.get('branch_id')
    
    # 권한에 따른 지점 필터링
    if user.admin_type == 'headquarters':
        # 본사 어드민: 전체 지점 또는 특정 지점
        if branch_id:
            branches = Branch.objects.filter(id=branch_id, is_active=True)
        else:
            branches = Branch.objects.filter(is_active=True)
    else:
        # 지점 어드민: 본인 지점만
        branches = Branch.objects.filter(id=user.branch.id, is_active=True)
    
    # 현재 월
    current_date = timezone.now().date()
    current_year = current_date.year
    current_month = current_date.month
    
    # 기본 통계
    total_members = Member.objects.filter(branch__in=branches).count()
    active_members = Member.objects.filter(
        branch__in=branches, 
        membership_status='active'
    ).count()
    
    total_trainers = Trainer.objects.filter(
        branch__in=branches, 
        employment_status='active'
    ).count()
    
    # 이번 달 예약 통계
    monthly_reservations = Reservation.objects.filter(
        trainer__branch__in=branches,
        date__year=current_year,
        date__month=current_month
    )
    
    confirmed_reservations = monthly_reservations.filter(
        reservation_status='confirmed'
    ).count()
    
    completed_reservations = monthly_reservations.filter(
        reservation_status='completed'
    ).count()
    
    # 이번 달 매출 통계
    monthly_revenue = BranchRevenue.objects.filter(
        branch__in=branches,
        year=current_year,
        month=current_month
    ).aggregate(
        total_pt_revenue=Sum('pt_revenue'),
        total_membership_revenue=Sum('membership_revenue'),
        total_additional_revenue=Sum('additional_revenue'),
        total_revenue=Sum('total_revenue')
    )
    
    # 이번 달 급여 통계
    monthly_salary = Salary.objects.filter(
        trainer__branch__in=branches,
        year=current_year,
        month=current_month
    ).aggregate(
        total_base_salary=Sum('base_salary'),
        total_incentive=Sum('incentive_amount'),
        total_additional_revenue=Sum('additional_revenue'),
        total_other_costs=Sum('other_costs'),
        total_salary=Sum('total_salary')
    )
    
    # 최근 알림
    recent_notifications = Notification.objects.filter(
        recipient_type='admin',
        recipient_id=user.id
    ).order_by('-created_at')[:5]
    
    notification_data = []
    for notification in recent_notifications:
        notification_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'created_at': notification.created_at,
            'is_read': notification.status == 'read'
        })
    
    return Response({
        'overview': {
            'total_members': total_members,
            'active_members': active_members,
            'total_trainers': total_trainers,
            'monthly_reservations': {
                'confirmed': confirmed_reservations,
                'completed': completed_reservations,
                'total': monthly_reservations.count()
            },
            'monthly_revenue': {
                'pt_revenue': float(monthly_revenue['total_pt_revenue'] or 0),
                'membership_revenue': float(monthly_revenue['total_membership_revenue'] or 0),
                'additional_revenue': float(monthly_revenue['total_additional_revenue'] or 0),
                'total_revenue': float(monthly_revenue['total_revenue'] or 0)
            },
            'monthly_salary': {
                'base_salary': float(monthly_salary['total_base_salary'] or 0),
                'incentive': float(monthly_salary['total_incentive'] or 0),
                'additional_revenue': float(monthly_salary['total_additional_revenue'] or 0),
                'other_costs': float(monthly_salary['total_other_costs'] or 0),
                'total_salary': float(monthly_salary['total_salary'] or 0)
            }
        },
        'recent_notifications': notification_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def revenue_chart(request):
    """매출 차트 데이터"""
    user = request.user
    branch_id = request.GET.get('branch_id')
    period = request.GET.get('period', 'monthly')  # monthly, yearly
    
    # 권한에 따른 지점 필터링
    if user.admin_type == 'headquarters':
        if branch_id:
            branches = Branch.objects.filter(id=branch_id, is_active=True)
        else:
            branches = Branch.objects.filter(is_active=True)
    else:
        branches = Branch.objects.filter(id=user.branch.id, is_active=True)
    
    current_date = timezone.now().date()
    
    if period == 'yearly':
        # 연간 데이터 (최근 12개월)
        data = []
        for i in range(12):
            target_date = current_date - timedelta(days=30*i)
            year = target_date.year
            month = target_date.month
            
            revenue = BranchRevenue.objects.filter(
                branch__in=branches,
                year=year,
                month=month
            ).aggregate(
                total_revenue=Sum('total_revenue'),
                pt_revenue=Sum('pt_revenue'),
                membership_revenue=Sum('membership_revenue')
            )
            
            data.append({
                'period': f"{year}-{month:02d}",
                'total_revenue': float(revenue['total_revenue'] or 0),
                'pt_revenue': float(revenue['pt_revenue'] or 0),
                'membership_revenue': float(revenue['membership_revenue'] or 0)
            })
        
        data.reverse()  # 시간순 정렬
    else:
        # 월간 데이터 (최근 30일)
        data = []
        for i in range(30):
            target_date = current_date - timedelta(days=i)
            
            # 해당 날짜의 PT 매출 계산
            pt_revenue = PTRecord.objects.filter(
                trainer__branch__in=branches,
                workout_date=target_date,
                is_completed=True
            ).aggregate(
                total_revenue=Sum('reservation__pt_registration__total_price')
            )
            
            data.append({
                'period': target_date.strftime('%Y-%m-%d'),
                'pt_revenue': float(pt_revenue['total_revenue'] or 0),
                'total_revenue': float(pt_revenue['total_revenue'] or 0)  # 간단히 PT 매출만
            })
        
        data.reverse()  # 시간순 정렬
    
    return Response({
        'period': period,
        'data': data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member_stats(request):
    """회원 통계"""
    user = request.user
    branch_id = request.GET.get('branch_id')
    
    # 권한에 따른 지점 필터링
    if user.admin_type == 'headquarters':
        if branch_id:
            branches = Branch.objects.filter(id=branch_id, is_active=True)
        else:
            branches = Branch.objects.filter(is_active=True)
    else:
        branches = Branch.objects.filter(id=user.branch.id, is_active=True)
    
    # 회원 상태별 통계
    membership_stats = Member.objects.filter(
        branch__in=branches
    ).values('membership_status').annotate(
        count=Count('id')
    )
    
    # 성별 통계
    gender_stats = Member.objects.filter(
        branch__in=branches
    ).values('gender').annotate(
        count=Count('id')
    )
    
    # 연령대별 통계 (생년월일 기준)
    current_year = timezone.now().year
    age_stats = []
    
    for age_range in [(20, 29), (30, 39), (40, 49), (50, 59), (60, 69), (70, 79)]:
        min_age, max_age = age_range
        min_birth_year = current_year - max_age
        max_birth_year = current_year - min_age
        
        count = Member.objects.filter(
            branch__in=branches,
            birth_date__year__gte=min_birth_year,
            birth_date__year__lte=max_birth_year
        ).count()
        
        age_stats.append({
            'age_range': f"{min_age}-{max_age}",
            'count': count
        })
    
    # 최근 가입 회원 (최근 30일)
    recent_members = Member.objects.filter(
        branch__in=branches,
        registration_date__gte=timezone.now().date() - timedelta(days=30)
    ).count()
    
    return Response({
        'membership_stats': list(membership_stats),
        'gender_stats': list(gender_stats),
        'age_stats': age_stats,
        'recent_members': recent_members
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trainer_stats(request):
    """트레이너 통계"""
    user = request.user
    branch_id = request.GET.get('branch_id')
    
    # 권한에 따른 지점 필터링
    if user.admin_type == 'headquarters':
        if branch_id:
            branches = Branch.objects.filter(id=branch_id, is_active=True)
        else:
            branches = Branch.objects.filter(is_active=True)
    else:
        branches = Branch.objects.filter(id=user.branch.id, is_active=True)
    
    # 트레이너별 PT 완료 통계 (이번 달)
    current_date = timezone.now().date()
    trainer_pt_stats = PTRecord.objects.filter(
        trainer__branch__in=branches,
        workout_date__year=current_date.year,
        workout_date__month=current_date.month,
        is_completed=True
    ).values('trainer__name').annotate(
        completed_sessions=Count('id'),
        total_duration=Sum('duration')
    ).order_by('-completed_sessions')
    
    # 트레이너별 인센티브 통계 (이번 달)
    trainer_incentive_stats = Salary.objects.filter(
        trainer__branch__in=branches,
        year=current_date.year,
        month=current_date.month
    ).values('trainer__name').annotate(
        base_salary=Sum('base_salary'),
        incentive_amount=Sum('incentive_amount'),
        total_salary=Sum('total_salary')
    ).order_by('-total_salary')
    
    # 경력별 트레이너 통계
    experience_stats = Trainer.objects.filter(
        branch__in=branches,
        employment_status='active'
    ).values('experience_years').annotate(
        count=Count('id')
    ).order_by('experience_years')
    
    return Response({
        'trainer_pt_stats': list(trainer_pt_stats),
        'trainer_incentive_stats': list(trainer_incentive_stats),
        'experience_stats': list(experience_stats)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reservation_stats(request):
    """예약 통계"""
    user = request.user
    branch_id = request.GET.get('branch_id')
    
    # 권한에 따른 지점 필터링
    if user.admin_type == 'headquarters':
        if branch_id:
            branches = Branch.objects.filter(id=branch_id, is_active=True)
        else:
            branches = Branch.objects.filter(is_active=True)
    else:
        branches = Branch.objects.filter(id=user.branch.id, is_active=True)
    
    # 예약 상태별 통계 (이번 달)
    current_date = timezone.now().date()
    reservation_status_stats = Reservation.objects.filter(
        trainer__branch__in=branches,
        date__year=current_date.year,
        date__month=current_date.month
    ).values('reservation_status').annotate(
        count=Count('id')
    )
    
    # 요일별 예약 통계
    weekday_stats = Reservation.objects.filter(
        trainer__branch__in=branches,
        date__year=current_date.year,
        date__month=current_date.month
    ).extra(
        select={'weekday': "EXTRACT(dow FROM date)"}
    ).values('weekday').annotate(
        count=Count('id')
    ).order_by('weekday')
    
    # 시간대별 예약 통계
    time_slot_stats = Reservation.objects.filter(
        trainer__branch__in=branches,
        date__year=current_date.year,
        date__month=current_date.month
    ).extra(
        select={'hour': "EXTRACT(hour FROM start_time)"}
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('hour')
    
    return Response({
        'reservation_status_stats': list(reservation_status_stats),
        'weekday_stats': list(weekday_stats),
        'time_slot_stats': list(time_slot_stats)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def branch_comparison(request):
    """지점별 비교 통계 (본사 어드민만)"""
    user = request.user
    
    if user.admin_type != 'headquarters':
        return Response(
            {'error': '본사 어드민만 접근 가능합니다.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    current_date = timezone.now().date()
    
    # 지점별 회원 수
    branch_member_stats = Member.objects.filter(
        membership_status='active'
    ).values('branch__name').annotate(
        member_count=Count('id')
    ).order_by('-member_count')
    
    # 지점별 트레이너 수
    branch_trainer_stats = Trainer.objects.filter(
        employment_status='active'
    ).values('branch__name').annotate(
        trainer_count=Count('id')
    ).order_by('-trainer_count')
    
    # 지점별 매출 (이번 달)
    branch_revenue_stats = BranchRevenue.objects.filter(
        year=current_date.year,
        month=current_date.month
    ).values('branch__name').annotate(
        total_revenue=Sum('total_revenue'),
        pt_revenue=Sum('pt_revenue'),
        membership_revenue=Sum('membership_revenue')
    ).order_by('-total_revenue')
    
    return Response({
        'branch_member_stats': list(branch_member_stats),
        'branch_trainer_stats': list(branch_trainer_stats),
        'branch_revenue_stats': list(branch_revenue_stats)
    })
