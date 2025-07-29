from rest_framework import serializers
from .models import Trainer, TrainerIncentive, TrainerSchedule, TrainerBlockedTime

class TrainerSerializer(serializers.ModelSerializer):
    """트레이너 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Trainer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TrainerIncentiveSerializer(serializers.ModelSerializer):
    """트레이너 인센티브 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    
    class Meta:
        model = TrainerIncentive
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TrainerScheduleSerializer(serializers.ModelSerializer):
    """트레이너 일정 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainerSchedule
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_day_name(self, obj):
        """요일 이름 반환"""
        days = ['월', '화', '수', '목', '금', '토', '일']
        return days[obj.day_of_week] if 0 <= obj.day_of_week < 7 else ''

class TrainerBlockedTimeSerializer(serializers.ModelSerializer):
    """트레이너 차단 시간 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    
    class Meta:
        model = TrainerBlockedTime
        fields = '__all__'
        read_only_fields = ('created_at',)

class TrainerDetailSerializer(serializers.ModelSerializer):
    """트레이너 상세 정보 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    incentive = TrainerIncentiveSerializer(read_only=True)
    schedules = TrainerScheduleSerializer(many=True, read_only=True)
    blocked_times = TrainerBlockedTimeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trainer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TrainerScheduleDetailSerializer(serializers.ModelSerializer):
    """트레이너 일정 상세 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    branch_name = serializers.CharField(source='trainer.branch.name', read_only=True)
    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainerSchedule
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_day_name(self, obj):
        """요일 이름 반환"""
        days = ['월', '화', '수', '목', '금', '토', '일']
        return days[obj.day_of_week] if 0 <= obj.day_of_week < 7 else '' 