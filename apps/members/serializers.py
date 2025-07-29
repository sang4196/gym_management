from rest_framework import serializers
from .models import Member, PTProgram, MemberPTRegistration

class MemberSerializer(serializers.ModelSerializer):
    """회원 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PTProgramSerializer(serializers.ModelSerializer):
    """PT 프로그램 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = PTProgram
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class MemberPTRegistrationSerializer(serializers.ModelSerializer):
    """회원 PT 등록 시리얼라이저"""
    member_name = serializers.CharField(source='member.name', read_only=True)
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    program_name = serializers.CharField(source='pt_program.name', read_only=True)
    completion_rate = serializers.CharField(source='get_completion_rate', read_only=True)
    
    class Meta:
        model = MemberPTRegistration
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class MemberDetailSerializer(serializers.ModelSerializer):
    """회원 상세 정보 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    pt_registrations = MemberPTRegistrationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PTProgramDetailSerializer(serializers.ModelSerializer):
    """PT 프로그램 상세 정보 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    active_registrations = serializers.SerializerMethodField()
    
    class Meta:
        model = PTProgram
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_active_registrations(self, obj):
        """활성 등록 수"""
        return obj.memberptregistration_set.filter(registration_status='active').count() 