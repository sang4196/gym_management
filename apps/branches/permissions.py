from rest_framework import permissions


class BranchPermission(permissions.BasePermission):
    """지점 관리 권한"""
    
    def has_permission(self, request, view):
        # 인증된 사용자만 접근 가능
        if not request.user.is_authenticated:
            return False
        
        # 본사 어드민은 모든 지점 관리 가능
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 어드민은 본인 지점만 관리 가능
        if request.user.admin_type == 'branch':
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # 본사 어드민은 모든 지점 관리 가능
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 어드민은 본인 지점만 관리 가능
        if request.user.admin_type == 'branch':
            return obj.id == request.user.branch.id
        
        return False


class BranchAdminPermission(permissions.BasePermission):
    """지점 어드민 관리 권한"""
    
    def has_permission(self, request, view):
        # 인증된 사용자만 접근 가능
        if not request.user.is_authenticated:
            return False
        
        # 본사 어드민만 어드민 관리 가능
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 어드민은 본인 정보만 수정 가능
        if request.user.admin_type == 'branch':
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # 본사 어드민은 모든 어드민 관리 가능
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 어드민은 본인 정보만 수정 가능
        if request.user.admin_type == 'branch':
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.id == request.user.id
        
        return False


class BranchStatsPermission(permissions.BasePermission):
    """지점 통계 권한"""
    
    def has_permission(self, request, view):
        # 인증된 사용자만 접근 가능
        if not request.user.is_authenticated:
            return False
        
        # 본사 어드민은 모든 지점 통계 조회 가능
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 어드민은 본인 지점 통계만 조회 가능
        if request.user.admin_type == 'branch':
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # 본사 어드민은 모든 지점 통계 조회 가능
        if request.user.admin_type == 'headquarters':
            return True
        
        # 지점 어드민은 본인 지점 통계만 조회 가능
        if request.user.admin_type == 'branch':
            return obj.id == request.user.branch.id
        
        return False 