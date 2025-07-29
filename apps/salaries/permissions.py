from rest_framework import permissions

class SalaryPermission(permissions.BasePermission):
    """
    급여 관련 권한 클래스
    - 본사 관리자: 모든 급여 접근 가능
    - 지점 관리자: 자신의 지점 급여만 접근 가능
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.trainer.branch == request.user.branch

class IncentiveDetailPermission(permissions.BasePermission):
    """인센티브 상세 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.salary.trainer.branch == request.user.branch

class AdditionalRevenuePermission(permissions.BasePermission):
    """추가 매출 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.salary.trainer.branch == request.user.branch

class OtherCostPermission(permissions.BasePermission):
    """기타 비용 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.salary.trainer.branch == request.user.branch

class BranchRevenuePermission(permissions.BasePermission):
    """지점 매출 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.branch == request.user.branch 