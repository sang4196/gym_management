from rest_framework import permissions

class ReservationPermission(permissions.BasePermission):
    """
    예약 관련 권한 클래스
    - 본사 관리자: 모든 예약 접근 가능
    - 지점 관리자: 자신의 지점 예약만 접근 가능
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
        
        return obj.member.branch == request.user.branch

class PTRecordPermission(permissions.BasePermission):
    """
    PT 기록 관련 권한 클래스
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
        
        return obj.member.branch == request.user.branch

class PTRecordImagePermission(permissions.BasePermission):
    """
    PT 기록 이미지 관련 권한 클래스
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
        
        return obj.pt_record.member.branch == request.user.branch

class ReservationChangeLogPermission(permissions.BasePermission):
    """
    예약 변경 로그 관련 권한 클래스
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
        
        return obj.reservation.member.branch == request.user.branch 