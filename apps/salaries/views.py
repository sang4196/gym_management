from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg
from datetime import date
from .models import Salary, IncentiveDetail, AdditionalRevenue, OtherCost, BranchRevenue
from .serializers import (
    SalarySerializer,
    IncentiveDetailSerializer,
    AdditionalRevenueSerializer,
    OtherCostSerializer,
    BranchRevenueSerializer,
    SalaryDetailSerializer,
    BranchRevenueDetailSerializer
)
from .permissions import (
    SalaryPermission,
    IncentiveDetailPermission,
    AdditionalRevenuePermission,
    OtherCostPermission,
    BranchRevenuePermission
)

class SalaryViewSet(viewsets.ModelViewSet):
    """급여 API 뷰셋"""
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [SalaryPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['trainer', 'year', 'month', 'payment_status']
    search_fields = ['trainer__name']
    ordering_fields = ['year', 'month', 'total_salary', 'payment_date']
    ordering = ['-year', '-month']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return Salary.objects.all()
        else:
            return Salary.objects.filter(trainer__branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return SalaryDetailSerializer
        return SalarySerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """급여 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_salaries': queryset.count(),
            'paid_salaries': queryset.filter(payment_status='paid').count(),
            'pending_salaries': queryset.filter(payment_status='pending').count(),
            'total_paid_amount': queryset.filter(payment_status='paid').aggregate(
                total=Sum('total_salary')
            )['total'] or 0,
            'average_salary': queryset.aggregate(avg=Avg('total_salary'))['avg'] or 0,
            'monthly_distribution': queryset.values('year', 'month').annotate(
                count=Count('id'),
                total_amount=Sum('total_salary')
            ).order_by('-year', '-month'),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def current_month(self, request):
        """현재 월 급여 조회"""
        current_year = date.today().year
        current_month = date.today().month
        
        current_salaries = self.get_queryset().filter(
            year=current_year,
            month=current_month
        )
        serializer = self.get_serializer(current_salaries, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """급여 지급 처리"""
        salary = self.get_object()
        salary.payment_status = 'paid'
        salary.payment_date = date.today()
        salary.save()
        
        return Response({'message': '급여가 지급되었습니다.'})

class IncentiveDetailViewSet(viewsets.ModelViewSet):
    """인센티브 상세 API 뷰셋"""
    queryset = IncentiveDetail.objects.all()
    serializer_class = IncentiveDetailSerializer
    permission_classes = [IncentiveDetailPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['salary', 'incentive_type']
    search_fields = ['description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return IncentiveDetail.objects.all()
        else:
            return IncentiveDetail.objects.filter(salary__trainer__branch=user.branch)

class AdditionalRevenueViewSet(viewsets.ModelViewSet):
    """추가 매출 API 뷰셋"""
    queryset = AdditionalRevenue.objects.all()
    serializer_class = AdditionalRevenueSerializer
    permission_classes = [AdditionalRevenuePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['salary', 'revenue_type']
    search_fields = ['description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return AdditionalRevenue.objects.all()
        else:
            return AdditionalRevenue.objects.filter(salary__trainer__branch=user.branch)

class OtherCostViewSet(viewsets.ModelViewSet):
    """기타 비용 API 뷰셋"""
    queryset = OtherCost.objects.all()
    serializer_class = OtherCostSerializer
    permission_classes = [OtherCostPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['salary', 'cost_type']
    search_fields = ['description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return OtherCost.objects.all()
        else:
            return OtherCost.objects.filter(salary__trainer__branch=user.branch)

class BranchRevenueViewSet(viewsets.ModelViewSet):
    """지점 매출 API 뷰셋"""
    queryset = BranchRevenue.objects.all()
    serializer_class = BranchRevenueSerializer
    permission_classes = [BranchRevenuePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'year', 'month']
    search_fields = ['branch__name']
    ordering_fields = ['year', 'month', 'total_revenue']
    ordering = ['-year', '-month']
    
    def get_queryset(self):
        """사용자 권한에 따른 쿼리셋 필터링"""
        user = self.request.user
        if user.admin_type == 'headquarters':
            return BranchRevenue.objects.all()
        else:
            return BranchRevenue.objects.filter(branch=user.branch)
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 선택"""
        if self.action == 'retrieve':
            return BranchRevenueDetailSerializer
        return BranchRevenueSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """지점 매출 통계 정보"""
        queryset = self.get_queryset()
        
        stats = {
            'total_revenues': queryset.count(),
            'total_pt_revenue': queryset.aggregate(total=Sum('pt_revenue'))['total'] or 0,
            'total_membership_revenue': queryset.aggregate(total=Sum('membership_revenue'))['total'] or 0,
            'total_additional_revenue': queryset.aggregate(total=Sum('additional_revenue'))['total'] or 0,
            'total_revenue_sum': queryset.aggregate(total=Sum('total_revenue'))['total'] or 0,
            'monthly_distribution': queryset.values('year', 'month').annotate(
                total_revenue=Sum('total_revenue'),
                total_pt_revenue=Sum('pt_revenue'),
                total_membership_revenue=Sum('membership_revenue')
            ).order_by('-year', '-month'),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def current_month(self, request):
        """현재 월 매출 조회"""
        current_year = date.today().year
        current_month = date.today().month
        
        current_revenues = self.get_queryset().filter(
            year=current_year,
            month=current_month
        )
        serializer = self.get_serializer(current_revenues, many=True)
        return Response(serializer.data)
