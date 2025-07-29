from rest_framework import serializers
from .models import Branch, BranchAdmin

class BranchSerializer(serializers.ModelSerializer):
    """지점 시리얼라이저"""
    
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class BranchAdminSerializer(serializers.ModelSerializer):
    """지점 관리자 시리얼라이저"""
    branch_name = serializers.CharField(source='get_branch_name', read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = BranchAdmin
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'branch', 'branch_name', 'admin_type', 'phone', 'is_active',
            'date_joined', 'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class BranchAdminCreateSerializer(serializers.ModelSerializer):
    """지점 관리자 생성용 시리얼라이저"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = BranchAdmin
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'branch', 'admin_type', 'phone'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = BranchAdmin.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user 