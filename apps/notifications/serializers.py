from rest_framework import serializers
from .models import Notification, NotificationTemplate, NotificationLog

class NotificationSerializer(serializers.ModelSerializer):
    """알림 시리얼라이저"""
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at')

class NotificationTemplateSerializer(serializers.ModelSerializer):
    """알림 템플릿 시리얼라이저"""
    
    class Meta:
        model = NotificationTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class NotificationLogSerializer(serializers.ModelSerializer):
    """알림 로그 시리얼라이저"""
    notification_info = serializers.CharField(source='notification', read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = '__all__'
        read_only_fields = ('created_at',)

class NotificationDetailSerializer(serializers.ModelSerializer):
    """알림 상세 정보 시리얼라이저"""
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    logs = NotificationLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at', 'sent_at')

class NotificationTemplateDetailSerializer(serializers.ModelSerializer):
    """알림 템플릿 상세 정보 시리얼라이저"""
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NotificationTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_usage_count(self, obj):
        """템플릿 사용 횟수"""
        return obj.notification_set.count() 