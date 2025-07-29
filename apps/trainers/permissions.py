from rest_framework import permissions

class TrainerPermission(permissions.BasePermission):
    """
    트레이너 관련 권한 클래스
    - 본사 관리자: 모든 트레이너 접근 가능
    - 지점 관리자: 자신의 지점 트레이너만 접근 가능
    """
    
    def has_permission(self, request, view):
        # 인증된 사용자만 접근 가능
        if not request.user.is_authenticated:
            return False
        
        # 본사 관리자는 모든 권한
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 관리자는 모든 권한
        return True
    
    def has_object_permission(self, request, view, obj):
        # 본사 관리자는 모든 권한
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 관리자는 자신의 지점 트레이너만 접근 가능
        return obj.branch == request.user.branch

class TrainerIncentivePermission(permissions.BasePermission):
    """
    트레이너 인센티브 관련 권한 클래스
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

class TrainerSchedulePermission(permissions.BasePermission):
    """
    트레이너 일정 관련 권한 클래스
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

class TrainerBlockedTimePermission(permissions.BasePermission):
    """
    트레이너 차단 시간 관련 권한 클래스
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