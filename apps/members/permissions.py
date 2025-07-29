from rest_framework import permissions

class MemberPermission(permissions.BasePermission):
    """
    회원 관련 권한 클래스
    - 본사 관리자: 모든 회원 접근 가능
    - 지점 관리자: 자신의 지점 회원만 접근 가능
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
        
        # 지점 관리자는 자신의 지점 회원만 접근 가능
        return obj.branch == request.user.branch

class PTProgramPermission(permissions.BasePermission):
    """
    PT 프로그램 관련 권한 클래스
    - 본사 관리자: 모든 프로그램 접근 가능
    - 지점 관리자: 자신의 지점 프로그램만 접근 가능
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
        
        # 지점 관리자는 자신의 지점 프로그램만 접근 가능
        return obj.branch == request.user.branch

class MemberPTRegistrationPermission(permissions.BasePermission):
    """
    회원 PT 등록 관련 권한 클래스
    - 본사 관리자: 모든 등록 접근 가능
    - 지점 관리자: 자신의 지점 등록만 접근 가능
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
        
        # 지점 관리자는 자신의 지점 등록만 접근 가능
        return obj.member.branch == request.user.branch 