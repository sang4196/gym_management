from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from .models import Member, PTProgram, MemberPTRegistration
from .serializers import (
    MemberSerializer, 
    PTProgramSerializer, 
    MemberPTRegistrationSerializer,
    MemberDetailSerializer,
    PTProgramDetailSerializer
)
from .permissions import MemberPermission, PTProgramPermission, MemberPTRegistrationPermission

class MemberViewSet(viewsets.ModelViewSet):
    """회원 API 뷰셋"""
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [MemberPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['membership_status', 'gender', 'branch']
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['name', 'registration_date', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return Member.objects.all()
        else:
            return Member.objects.filter(branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return MemberDetailSerializer
        return MemberSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """회원 통계 정보"""
        queryset = self.get_queryset()
        
        # 현재 월의 신규 회원 수 계산
        from django.utils import timezone
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        monthly_registrations = queryset.filter(
            registration_date__year=current_year,
            registration_date__month=current_month
        ).count()
        
        stats = {
            'total_members': queryset.count(),
            'active_members': queryset.filter(membership_status='active').count(),
            'expired_members': queryset.filter(membership_status='expired').count(),
            'gender_distribution': queryset.values('gender').annotate(count=Count('id')),
            'monthly_registrations': monthly_registrations,
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def pt_history(self, request, pk=None):
        """회원 PT 이력"""
        member = self.get_object()
        registrations = member.memberptregistration_set.all()
        serializer = MemberPTRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

class PTProgramViewSet(viewsets.ModelViewSet):
    """PT 프로그램 API 뷰셋"""
    queryset = PTProgram.objects.all()
    serializer_class = PTProgramSerializer
    permission_classes = [PTProgramPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['program_type', 'is_active', 'branch']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'sessions', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return PTProgram.objects.all()
        else:
            return PTProgram.objects.filter(branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return PTProgramDetailSerializer
        return PTProgramSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """PT 프로그램 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_programs': queryset.count(),
            'active_programs': queryset.filter(is_active=True).count(),
            'program_types': queryset.values('program_type').annotate(count=Count('id')),
            'total_revenue': queryset.aggregate(
                total=Sum('memberptregistration__total_price')
            )['total'] or 0,
        }
        
        return Response(stats)

class MemberPTRegistrationViewSet(viewsets.ModelViewSet):
    """회원 PT 등록 API 뷰셋"""
    queryset = MemberPTRegistration.objects.all()
    serializer_class = MemberPTRegistrationSerializer
    permission_classes = [MemberPTRegistrationPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['registration_status', 'member', 'trainer', 'pt_program']
    search_fields = ['member__name', 'trainer__name', 'pt_program__name']
    ordering_fields = ['registration_date', 'expiry_date', 'created_at']
    ordering = ['-registration_date']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return MemberPTRegistration.objects.all()
        else:
            return MemberPTRegistration.objects.filter(member__branch=user.branch)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """PT 등록 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_registrations': queryset.count(),
            'active_registrations': queryset.filter(registration_status='active').count(),
            'completed_registrations': queryset.filter(registration_status='completed').count(),
            'total_revenue': queryset.aggregate(total=Sum('total_price'))['total'] or 0,
            'average_completion_rate': queryset.aggregate(
                avg_rate=Sum('remaining_sessions') * 100.0 / Sum('total_sessions')
            )['avg_rate'] or 0,
        }
        
        return Response(stats)
