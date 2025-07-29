from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Notification, NotificationTemplate, NotificationLog
from .serializers import (
    NotificationSerializer,
    NotificationTemplateSerializer,
    NotificationLogSerializer,
    NotificationDetailSerializer,
    NotificationTemplateDetailSerializer
)
from .permissions import (
    NotificationPermission,
    NotificationTemplatePermission,
    NotificationLogPermission
)

class NotificationViewSet(viewsets.ModelViewSet):
    """알림 API 뷰셋"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [NotificationPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'status', 'recipient', 'sender']
    search_fields = ['title', 'message', 'recipient__username']
    ordering_fields = ['created_at', 'sent_at', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return Notification.objects.all()
        else:
            return Notification.objects.filter(recipient__branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return NotificationSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """알림 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_notifications': queryset.count(),
            'sent_notifications': queryset.filter(status='sent').count(),
            'pending_notifications': queryset.filter(status='pending').count(),
            'failed_notifications': queryset.filter(status='failed').count(),
            'today_notifications': queryset.filter(created_at__date=date.today()).count(),
            'this_week_notifications': queryset.filter(
                created_at__date__gte=date.today() - timedelta(days=7)
            ).count(),
            'type_distribution': queryset.values('notification_type').annotate(count=Count('id')),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """읽지 않은 알림 조회"""
        unread_notifications = self.get_queryset().filter(
            status='sent',
            is_read=False
        ).order_by('-created_at')
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """알림 읽음 처리"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        return Response({'message': '알림이 읽음 처리되었습니다.'})
    
    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        """알림 재전송"""
        notification = self.get_object()
        notification.status = 'pending'
        notification.sent_at = None
        notification.save()
        
        return Response({'message': '알림이 재전송 대기열에 추가되었습니다.'})

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """알림 템플릿 API 뷰셋"""
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [NotificationTemplatePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_active']
    search_fields = ['name', 'title_template', 'message_template']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return NotificationTemplateDetailSerializer
        return NotificationTemplateSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """알림 템플릿 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_templates': queryset.count(),
            'active_templates': queryset.filter(is_active=True).count(),
            'type_distribution': queryset.values('notification_type').annotate(count=Count('id')),
            'most_used_templates': queryset.annotate(
                usage_count=Count('notification')
            ).order_by('-usage_count')[:5],
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """템플릿 테스트"""
        template = self.get_object()
        
        # 테스트 데이터로 템플릿 렌더링
        test_data = {
            'member_name': '테스트 회원',
            'trainer_name': '테스트 트레이너',
            'date': date.today().strftime('%Y-%m-%d'),
            'time': '14:00'
        }
        
        try:
            title = template.title_template.format(**test_data)
            message = template.message_template.format(**test_data)
            
            return Response({
                'title': title,
                'message': message,
                'test_data': test_data
            })
        except KeyError as e:
            return Response(
                {'error': f'템플릿에 필요한 변수가 누락되었습니다: {e}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """알림 로그 API 뷰셋 (읽기 전용)"""
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    permission_classes = [NotificationLogPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification', 'log_type', 'status']
    search_fields = ['message', 'error_message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return NotificationLog.objects.all()
        else:
            return NotificationLog.objects.filter(notification__recipient__branch=user.branch)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """최근 로그 조회"""
        recent_logs = self.get_queryset().order_by('-created_at')[:100]
        serializer = self.get_serializer(recent_logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def errors(self, request):
        """에러 로그 조회"""
        error_logs = self.get_queryset().filter(
            status='error'
        ).order_by('-created_at')
        serializer = self.get_serializer(error_logs, many=True)
        return Response(serializer.data)
