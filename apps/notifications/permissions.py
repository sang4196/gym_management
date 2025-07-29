from rest_framework import permissions

class NotificationPermission(permissions.BasePermission):
    """
    알림 관련 권한 클래스
    - 본사 관리자: 모든 알림 접근 가능
    - 지점 관리자: 자신의 지점 알림만 접근 가능
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
        
        # 지점 관리자는 자신의 지점 관련 알림만 접근 가능
        if hasattr(obj.recipient, 'branch'):
            return obj.recipient.branch == request.user.branch
        return True

class NotificationTemplatePermission(permissions.BasePermission):
    """알림 템플릿 관련 권한 클래스"""
    
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

class NotificationLogPermission(permissions.BasePermission):
    """알림 로그 관련 권한 클래스"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.admin_type == 'headquarters':
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 관리자는 자신의 지점 관련 로그만 접근 가능
        if hasattr(obj.notification.recipient, 'branch'):
            return obj.notification.recipient.branch == request.user.branch
        return True 