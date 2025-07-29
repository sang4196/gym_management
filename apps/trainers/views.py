from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg
from datetime import date, timedelta
from .models import Trainer, TrainerIncentive, TrainerSchedule, TrainerBlockedTime
from .serializers import (
    TrainerSerializer,
    TrainerIncentiveSerializer,
    TrainerScheduleSerializer,
    TrainerBlockedTimeSerializer,
    TrainerDetailSerializer,
    TrainerScheduleDetailSerializer
)
from .permissions import (
    TrainerPermission,
    TrainerIncentivePermission,
    TrainerSchedulePermission,
    TrainerBlockedTimePermission
)

class TrainerViewSet(viewsets.ModelViewSet):
    """트레이너 API 뷰셋"""
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [TrainerPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employment_status', 'gender', 'branch']
    search_fields = ['name', 'phone', 'email', 'specialties']
    ordering_fields = ['name', 'hire_date', 'experience_years', 'base_salary']
    ordering = ['name']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return Trainer.objects.all()
        else:
            return Trainer.objects.filter(branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return TrainerDetailSerializer
        return TrainerSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """트레이너 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_trainers': queryset.count(),
            'active_trainers': queryset.filter(employment_status='active').count(),
            'gender_distribution': queryset.values('gender').annotate(count=Count('id')),
            'experience_distribution': queryset.values('experience_years').annotate(count=Count('id')),
            'average_salary': queryset.aggregate(avg_salary=Avg('base_salary'))['avg_salary'] or 0,
            'total_salary': queryset.aggregate(total_salary=Sum('base_salary'))['total_salary'] or 0,
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """트레이너 일정 조회"""
        trainer = self.get_object()
        schedules = trainer.trainerschedule_set.all()
        serializer = TrainerScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def blocked_times(self, request, pk=None):
        """트레이너 차단 시간 조회"""
        trainer = self.get_object()
        blocked_times = trainer.trainerblockedtime_set.all()
        serializer = TrainerBlockedTimeSerializer(blocked_times, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """트레이너 가용 시간 조회"""
        trainer = self.get_object()
        target_date = request.query_params.get('date', date.today())
        
        # 해당 날짜의 요일
        if isinstance(target_date, str):
            target_date = date.fromisoformat(target_date)
        
        day_of_week = target_date.weekday()
        
        # 해당 요일의 일정
        try:
            schedule = trainer.trainerschedule_set.get(day_of_week=day_of_week)
        except TrainerSchedule.DoesNotExist:
            return Response({'available': False, 'message': '해당 요일에는 일정이 없습니다.'})
        
        # 해당 날짜의 차단 시간
        blocked_times = trainer.trainerblockedtime_set.filter(date=target_date)
        
        availability = {
            'date': target_date,
            'day_of_week': day_of_week,
            'schedule': TrainerScheduleSerializer(schedule).data,
            'blocked_times': TrainerBlockedTimeSerializer(blocked_times, many=True).data,
            'available': schedule.is_available and not blocked_times.exists()
        }
        
        return Response(availability)

class TrainerIncentiveViewSet(viewsets.ModelViewSet):
    """트레이너 인센티브 API 뷰셋"""
    queryset = TrainerIncentive.objects.all()
    serializer_class = TrainerIncentiveSerializer
    permission_classes = [TrainerIncentivePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['incentive_type', 'is_active', 'trainer']
    search_fields = ['trainer__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return TrainerIncentive.objects.all()
        else:
            return TrainerIncentive.objects.filter(trainer__branch=user.branch)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """인센티브 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_incentives': queryset.count(),
            'active_incentives': queryset.filter(is_active=True).count(),
            'incentive_types': queryset.values('incentive_type').annotate(count=Count('id')),
            'average_fixed_amount': queryset.filter(incentive_type='fixed').aggregate(
                avg_amount=Avg('fixed_amount')
            )['avg_amount'] or 0,
            'average_percentage_rate': queryset.filter(incentive_type='percentage').aggregate(
                avg_rate=Avg('percentage_rate')
            )['avg_rate'] or 0,
        }
        
        return Response(stats)

class TrainerScheduleViewSet(viewsets.ModelViewSet):
    """트레이너 일정 API 뷰셋"""
    queryset = TrainerSchedule.objects.all()
    serializer_class = TrainerScheduleSerializer
    permission_classes = [TrainerSchedulePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['day_of_week', 'is_available', 'trainer']
    search_fields = ['trainer__name']
    ordering_fields = ['day_of_week', 'start_time', 'end_time']
    ordering = ['trainer__name', 'day_of_week']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return TrainerSchedule.objects.all()
        else:
            return TrainerSchedule.objects.filter(trainer__branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return TrainerScheduleDetailSerializer
        return TrainerScheduleSerializer
    
    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """주간 일정 조회"""
        trainer_id = request.query_params.get('trainer')
        if trainer_id:
            schedules = self.get_queryset().filter(trainer_id=trainer_id)
        else:
            schedules = self.get_queryset()
        
        # 요일별로 그룹화
        weekly_schedule = {}
        for schedule in schedules:
            day = schedule.day_of_week
            if day not in weekly_schedule:
                weekly_schedule[day] = []
            weekly_schedule[day].append(TrainerScheduleSerializer(schedule).data)
        
        return Response(weekly_schedule)

class TrainerBlockedTimeViewSet(viewsets.ModelViewSet):
    """트레이너 차단 시간 API 뷰셋"""
    queryset = TrainerBlockedTime.objects.all()
    serializer_class = TrainerBlockedTimeSerializer
    permission_classes = [TrainerBlockedTimePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['trainer', 'date']
    search_fields = ['trainer__name', 'reason']
    ordering_fields = ['date', 'start_time', 'end_time']
    ordering = ['-date', 'start_time']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return TrainerBlockedTime.objects.all()
        else:
            return TrainerBlockedTime.objects.filter(trainer__branch=user.branch)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """다가오는 차단 시간 조회"""
        today = date.today()
        upcoming_blocked = self.get_queryset().filter(date__gte=today).order_by('date', 'start_time')
        serializer = self.get_serializer(upcoming_blocked, many=True)
        return Response(serializer.data)
