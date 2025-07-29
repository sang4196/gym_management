from rest_framework import serializers
from .models import (
    DashboardWidget, DashboardLayout, UserDashboard, 
    UserDashboardWidget, Report, ReportExecution
)

class DashboardWidgetSerializer(serializers.ModelSerializer):
    """대시보드 위젯 시리얼라이저"""
    
    class Meta:
        model = DashboardWidget
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class DashboardLayoutSerializer(serializers.ModelSerializer):
    """대시보드 레이아웃 시리얼라이저"""
    
    class Meta:
        model = DashboardLayout
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class UserDashboardSerializer(serializers.ModelSerializer):
    """사용자 대시보드 시리얼라이저"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserDashboard
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class UserDashboardWidgetSerializer(serializers.ModelSerializer):
    """사용자 대시보드 위젯 시리얼라이저"""
    widget_name = serializers.CharField(source='widget.name', read_only=True)
    dashboard_name = serializers.CharField(source='dashboard.name', read_only=True)
    
    class Meta:
        model = UserDashboardWidget
        fields = '__all__'
        read_only_fields = ('created_at',)

class ReportSerializer(serializers.ModelSerializer):
    """리포트 시리얼라이저"""
    
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ReportExecutionSerializer(serializers.ModelSerializer):
    """리포트 실행 시리얼라이저"""
    report_name = serializers.CharField(source='report.name', read_only=True)
    executed_by_name = serializers.CharField(source='executed_by.username', read_only=True)
    
    class Meta:
        model = ReportExecution
        fields = '__all__'
        read_only_fields = ('created_at',)

class UserDashboardDetailSerializer(serializers.ModelSerializer):
    """사용자 대시보드 상세 정보 시리얼라이저"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    widgets = UserDashboardWidgetSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserDashboard
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ReportDetailSerializer(serializers.ModelSerializer):
    """리포트 상세 정보 시리얼라이저"""
    execution_count = serializers.SerializerMethodField()
    last_execution = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_execution_count(self, obj):
        """실행 횟수"""
        return obj.reportexecution_set.count()
    
    def get_last_execution(self, obj):
        """마지막 실행 정보"""
        last_exec = obj.reportexecution_set.order_by('-created_at').first()
        if last_exec:
            return {
                'id': last_exec.id,
                'status': last_exec.status,
                'created_at': last_exec.created_at,
                'executed_by': last_exec.executed_by.username
            }
        return None 