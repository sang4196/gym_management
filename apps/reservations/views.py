from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Q
from datetime import date, timedelta
from .models import Reservation, PTRecord, PTRecordImage, ReservationChangeLog
from .serializers import (
    ReservationSerializer,
    PTRecordSerializer,
    PTRecordImageSerializer,
    ReservationChangeLogSerializer,
    ReservationDetailSerializer,
    PTRecordDetailSerializer
)
from .permissions import (
    ReservationPermission,
    PTRecordPermission,
    PTRecordImagePermission,
    ReservationChangeLogPermission
)

class ReservationViewSet(viewsets.ModelViewSet):
    """예약 API 뷰셋"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [ReservationPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['reservation_status', 'member', 'trainer', 'pt_registration']
    search_fields = ['member__name', 'trainer__name', 'notes']
    ordering_fields = ['date', 'start_time', 'created_at']
    ordering = ['-date', 'start_time']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return Reservation.objects.all()
        else:
            return Reservation.objects.filter(member__branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return ReservationDetailSerializer
        return ReservationSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """예약 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_reservations': queryset.count(),
            'confirmed_reservations': queryset.filter(reservation_status='confirmed').count(),
            'completed_reservations': queryset.filter(reservation_status='completed').count(),
            'cancelled_reservations': queryset.filter(reservation_status='cancelled').count(),
            'today_reservations': queryset.filter(date=date.today()).count(),
            'upcoming_reservations': queryset.filter(date__gte=date.today()).count(),
            'status_distribution': queryset.values('reservation_status').annotate(count=Count('id')),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """오늘 예약 조회"""
        today_reservations = self.get_queryset().filter(date=date.today()).order_by('start_time')
        serializer = self.get_serializer(today_reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """다가오는 예약 조회"""
        upcoming_reservations = self.get_queryset().filter(
            date__gte=date.today()
        ).order_by('date', 'start_time')
        serializer = self.get_serializer(upcoming_reservations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """예약 확정"""
        reservation = self.get_object()
        reservation.reservation_status = 'confirmed'
        reservation.save()
        
        # 변경 로그 기록
        ReservationChangeLog.objects.create(
            reservation=reservation,
            change_type='status_change',
            changed_by=request.user,
            previous_status='pending',
            new_status='confirmed',
            reason='관리자가 예약을 확정했습니다.'
        )
        
        return Response({'message': '예약이 확정되었습니다.'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """예약 취소"""
        reservation = self.get_object()
        previous_status = reservation.reservation_status
        reservation.reservation_status = 'cancelled'
        reservation.save()
        
        # 변경 로그 기록
        ReservationChangeLog.objects.create(
            reservation=reservation,
            change_type='status_change',
            changed_by=request.user,
            previous_status=previous_status,
            new_status='cancelled',
            reason=request.data.get('reason', '관리자가 예약을 취소했습니다.')
        )
        
        return Response({'message': '예약이 취소되었습니다.'})

class PTRecordViewSet(viewsets.ModelViewSet):
    """PT 기록 API 뷰셋"""
    queryset = PTRecord.objects.all()
    serializer_class = PTRecordSerializer
    permission_classes = [PTRecordPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['trainer', 'member', 'is_completed']
    search_fields = ['trainer__name', 'member__name', 'content', 'trainer_notes']
    ordering_fields = ['workout_date', 'workout_time', 'created_at']
    ordering = ['-workout_date', '-workout_time']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return PTRecord.objects.all()
        else:
            return PTRecord.objects.filter(member__branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return PTRecordDetailSerializer
        return PTRecordSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """PT 기록 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_records': queryset.count(),
            'completed_records': queryset.filter(is_completed=True).count(),
            'today_records': queryset.filter(workout_date=date.today()).count(),
            'this_week_records': queryset.filter(
                workout_date__gte=date.today() - timedelta(days=7)
            ).count(),
            'trainer_performance': queryset.values('trainer__name').annotate(
                total_records=Count('id'),
                completed_records=Count('id', filter=Q(is_completed=True))
            ),
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """PT 기록 완료 처리"""
        record = self.get_object()
        record.is_completed = True
        record.save()
        
        return Response({'message': 'PT 기록이 완료되었습니다.'})

class PTRecordImageViewSet(viewsets.ModelViewSet):
    """PT 기록 이미지 API 뷰셋"""
    queryset = PTRecordImage.objects.all()
    serializer_class = PTRecordImageSerializer
    permission_classes = [PTRecordImagePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pt_record']
    search_fields = ['description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return PTRecordImage.objects.all()
        else:
            return PTRecordImage.objects.filter(pt_record__member__branch=user.branch)

class ReservationChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    """예약 변경 로그 API 뷰셋 (읽기 전용)"""
    queryset = ReservationChangeLog.objects.all()
    serializer_class = ReservationChangeLogSerializer
    permission_classes = [ReservationChangeLogPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['reservation', 'change_type', 'changed_by']
    search_fields = ['reason']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return ReservationChangeLog.objects.all()
        else:
            return ReservationChangeLog.objects.filter(reservation__member__branch=user.branch)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """최근 변경 로그 조회"""
        recent_logs = self.get_queryset().order_by('-created_at')[:50]
        serializer = self.get_serializer(recent_logs, many=True)
        return Response(serializer.data)
