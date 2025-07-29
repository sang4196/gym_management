from rest_framework import serializers
from .models import Salary, IncentiveDetail, AdditionalRevenue, OtherCost, BranchRevenue

class SalarySerializer(serializers.ModelSerializer):
    """급여 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    branch_name = serializers.CharField(source='trainer.branch.name', read_only=True)
    
    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class IncentiveDetailSerializer(serializers.ModelSerializer):
    """인센티브 상세 시리얼라이저"""
    trainer_name = serializers.CharField(source='salary.trainer.name', read_only=True)
    
    class Meta:
        model = IncentiveDetail
        fields = '__all__'
        read_only_fields = ('created_at',)

class AdditionalRevenueSerializer(serializers.ModelSerializer):
    """추가 매출 시리얼라이저"""
    trainer_name = serializers.CharField(source='salary.trainer.name', read_only=True)
    
    class Meta:
        model = AdditionalRevenue
        fields = '__all__'
        read_only_fields = ('created_at',)

class OtherCostSerializer(serializers.ModelSerializer):
    """기타 비용 시리얼라이저"""
    trainer_name = serializers.CharField(source='salary.trainer.name', read_only=True)
    
    class Meta:
        model = OtherCost
        fields = '__all__'
        read_only_fields = ('created_at',)

class BranchRevenueSerializer(serializers.ModelSerializer):
    """지점 매출 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = BranchRevenue
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class SalaryDetailSerializer(serializers.ModelSerializer):
    """급여 상세 정보 시리얼라이저"""
    trainer_name = serializers.CharField(source='trainer.name', read_only=True)
    branch_name = serializers.CharField(source='trainer.branch.name', read_only=True)
    incentive_details = IncentiveDetailSerializer(many=True, read_only=True)
    additional_revenues = AdditionalRevenueSerializer(many=True, read_only=True)
    other_costs = OtherCostSerializer(many=True, read_only=True)
    
    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class BranchRevenueDetailSerializer(serializers.ModelSerializer):
    """지점 매출 상세 정보 시리얼라이저"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = BranchRevenue
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at') 