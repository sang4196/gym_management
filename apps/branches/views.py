from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Branch, BranchAdmin
from .serializers import (
    BranchSerializer, 
    BranchAdminSerializer, 
    BranchAdminCreateSerializer
)
from .permissions import BranchPermission, BranchAdminPermission

class CustomAuthToken(ObtainAuthToken):
    """커스텀 인증 토큰 뷰"""
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'admin_type': user.admin_type,
            'branch_id': user.branch.id if user.branch else None,
            'branch_name': user.get_branch_name(),
        })

class BranchViewSet(viewsets.ModelViewSet):
    """지점 API 뷰셋"""
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [BranchPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'address', 'phone', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return Branch.objects.all()
        else:
            return Branch.objects.filter(id=user.branch.id)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """지점 통계 정보"""
        branch = self.get_object()
        
        # 지점별 통계 데이터
        stats = {
            'total_members': branch.member_set.count(),
            'total_trainers': branch.trainer_set.count(),
            'active_pt_registrations': branch.memberptregistration_set.filter(
                registration_status='active'
            ).count(),
            'total_revenue': branch.branchrevenue_set.aggregate(
                total=models.Sum('total_revenue')
            )['total'] or 0,
        }
        
        return Response(stats)

class BranchAdminViewSet(viewsets.ModelViewSet):
    """지점 관리자 API 뷰셋"""
    queryset = BranchAdmin.objects.all()
    serializer_class = BranchAdminSerializer
    permission_classes = [BranchAdminPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['admin_type', 'is_active', 'branch']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined', 'last_login']
    ordering = ['username']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return BranchAdmin.objects.all()
        else:
            return BranchAdmin.objects.filter(branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'create':
            return BranchAdminCreateSerializer
        return BranchAdminSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """현재 로그인한 사용자 정보"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """비밀번호 변경"""
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {'error': '현재 비밀번호가 올바르지 않습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': '비밀번호가 변경되었습니다.'})
