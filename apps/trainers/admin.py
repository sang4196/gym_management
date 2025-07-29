from django.contrib import admin
from .models import Trainer, TrainerIncentive, TrainerSchedule, TrainerBlockedTime


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'phone', 'employment_status', 'base_salary', 'experience_years', 'hire_date']
    list_filter = ['branch', 'employment_status', 'gender', 'hire_date']
    search_fields = ['name', 'phone', 'email', 'specialties']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('branch', 'name', 'phone', 'email', 'birth_date', 'gender')
        }),
        ('주소 및 연락처', {
            'fields': ('address', 'emergency_contact')
        }),
        ('근무 정보', {
            'fields': ('employment_status', 'hire_date', 'base_salary', 'experience_years')
        }),
        ('전문 정보', {
            'fields': ('specialties', 'certifications', 'profile_image')
        }),
        ('카카오톡', {
            'fields': ('kakao_id',)
        }),
        ('메모', {
            'fields': ('notes',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrainerIncentive)
class TrainerIncentiveAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'incentive_type', 'fixed_amount', 'percentage_rate', 'is_active']
    list_filter = ['incentive_type', 'is_active', 'created_at']
    search_fields = ['trainer__name']
    ordering = ['trainer__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('트레이너', {
            'fields': ('trainer',)
        }),
        ('인센티브 설정', {
            'fields': ('incentive_type', 'fixed_amount', 'percentage_rate')
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrainerSchedule)
class TrainerScheduleAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'day_of_week', 'start_time', 'end_time', 'is_available']
    list_filter = ['trainer__branch', 'day_of_week', 'is_available']
    search_fields = ['trainer__name']
    ordering = ['trainer__name', 'day_of_week']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('트레이너', {
            'fields': ('trainer',)
        }),
        ('일정', {
            'fields': ('day_of_week', 'start_time', 'end_time', 'is_available')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrainerBlockedTime)
class TrainerBlockedTimeAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'date', 'start_time', 'end_time', 'reason', 'created_at']
    list_filter = ['trainer__branch', 'date']
    search_fields = ['trainer__name', 'reason']
    ordering = ['-date', 'start_time']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('트레이너', {
            'fields': ('trainer',)
        }),
        ('차단 시간', {
            'fields': ('date', 'start_time', 'end_time', 'reason')
        }),
        ('생성일', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
