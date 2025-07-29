from rest_framework import serializers
from .models import Reservation, PTRecord, PTRecordImage, ReservationChangeLog

class ReservationSerializer(serializers.ModelSerializer):
    """예약 시리얼라이저"""
    member_name = serializers.CharField(source='member.name', read_only=True)
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    program_name = serializers.CharField(source='pt_registration.pt_program.name', read_only=True)
    branch_name = serializers.CharField(source='member.branch.name', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PTRecordSerializer(serializers.ModelSerializer):
    """PT 기록 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)
    reservation_info = serializers.CharField(source='reservation', read_only=True)
    
    class Meta:
        model = PTRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PTRecordImageSerializer(serializers.ModelSerializer):
    """PT 기록 이미지 시리얼라이저"""
    record_info = serializers.CharField(source='pt_record', read_only=True)
    
    class Meta:
        model = PTRecordImage
        fields = '__all__'
        read_only_fields = ('created_at',)

class ReservationChangeLogSerializer(serializers.ModelSerializer):
    """예약 변경 로그 시리얼라이저"""
    reservation_info = serializers.CharField(source='reservation', read_only=True)
    changed_by_name = serializers.CharField(source='changed_by.username', read_only=True)
    
    class Meta:
        model = ReservationChangeLog
        fields = '__all__'
        read_only_fields = ('created_at',)

class ReservationDetailSerializer(serializers.ModelSerializer):
    """예약 상세 정보 시리얼라이저"""
    member_name = serializers.CharField(source='member.name', read_only=True)
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    program_name = serializers.CharField(source='pt_registration.pt_program.name', read_only=True)
    branch_name = serializers.CharField(source='member.branch.name', read_only=True)
    pt_record = PTRecordSerializer(read_only=True)
    change_logs = ReservationChangeLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PTRecordDetailSerializer(serializers.ModelSerializer):
    """PT 기록 상세 정보 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    member_name = serializers.CharField(source='member.name', read_only=True)
    reservation_info = serializers.CharField(source='reservation', read_only=True)
    images = PTRecordImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = PTRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at') 