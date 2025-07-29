from rest_framework import permissions

class DashboardWidgetPermission(permissions.BasePermission):
    """대시보드 위젯 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return True

class DashboardLayoutPermission(permissions.BasePermission):
    """대시보드 레이아웃 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return True

class UserDashboardPermission(permissions.BasePermission):
    """사용자 대시보드 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.user == request.user

class UserDashboardWidgetPermission(permissions.BasePermission):
    """사용자 대시보드 위젯 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.dashboard.user == request.user

class ReportPermission(permissions.BasePermission):
    """리포트 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return True

class ReportExecutionPermission(permissions.BasePermission):
    """리포트 실행 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        return obj.executed_by == request.user 