from django.contrib import admin
from .models import Salary, IncentiveDetail, AdditionalRevenue, OtherCost, BranchRevenue


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'year', 'month', 'base_salary', 'incentive_amount', 'total_salary', 'payment_status']
    list_filter = ['year', 'month', 'payment_status', 'trainer']
    search_fields = ['trainer__name']
    ordering = ['-year', '-month', 'trainer__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('trainer', 'year', 'month')
        }),
        ('급여 구성', {
            'fields': ('base_salary', 'incentive_amount', 'additional_revenue', 'other_costs', 'total_salary')
        }),
        ('지급 정보', {
            'fields': ('payment_status', 'payment_date', 'notes')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def branch(self, obj):
        return obj.trainer.branch.name
    branch.short_description = '지점'


@admin.register(IncentiveDetail)
class IncentiveDetailAdmin(admin.ModelAdmin):
    list_display = ['salary', 'incentive_type', 'quantity', 'unit_amount', 'total_amount']
    list_filter = ['incentive_type', 'created_at']
    search_fields = ['salary__trainer__name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('급여', {
            'fields': ('salary',)
        }),
        ('인센티브 정보', {
            'fields': ('incentive_type', 'quantity', 'unit_amount', 'total_amount', 'description')
        }),
        ('생성일', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdditionalRevenue)
class AdditionalRevenueAdmin(admin.ModelAdmin):
    list_display = ['salary', 'revenue_type', 'amount', 'created_at']
    list_filter = ['revenue_type', 'created_at']
    search_fields = ['salary__trainer__name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('급여', {
            'fields': ('salary',)
        }),
        ('매출 정보', {
            'fields': ('revenue_type', 'amount', 'description')
        }),
        ('생성일', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(OtherCost)
class OtherCostAdmin(admin.ModelAdmin):
    list_display = ['salary', 'cost_type', 'amount', 'created_at']
    list_filter = ['cost_type', 'created_at']
    search_fields = ['salary__trainer__name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('급여', {
            'fields': ('salary',)
        }),
        ('비용 정보', {
            'fields': ('cost_type', 'amount', 'description')
        }),
        ('생성일', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(BranchRevenue)
class BranchRevenueAdmin(admin.ModelAdmin):
    list_display = ['branch', 'year', 'month', 'pt_revenue', 'membership_revenue', 'total_revenue']
    list_filter = ['year', 'month']
    search_fields = ['branch__name']
    ordering = ['-year', '-month', 'branch__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('branch', 'year', 'month')
        }),
        ('매출 구성', {
            'fields': ('pt_revenue', 'membership_revenue', 'additional_revenue', 'total_revenue')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
