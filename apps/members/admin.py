from django.contrib import admin
from .models import Member, PTProgram, MemberPTRegistration


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'phone', 'membership_status', 'registration_date', 'expiry_date']
    list_filter = ['membership_status', 'gender', 'registration_date']
    search_fields = ['name', 'phone', 'email']
    ordering = ['-registration_date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('branch', 'name', 'phone', 'email', 'birth_date', 'gender')
        }),
        ('주소 및 연락처', {
            'fields': ('address', 'emergency_contact')
        }),
        ('회원 정보', {
            'fields': ('membership_status', 'registration_date', 'expiry_date')
        }),
        ('메모', {
            'fields': ('notes',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PTProgram)
class PTProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'program_type', 'sessions', 'price', 'is_active']
    list_filter = ['branch', 'program_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('branch', 'name', 'program_type', 'description')
        }),
        ('프로그램 설정', {
            'fields': ('sessions', 'price')
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MemberPTRegistration)
class MemberPTRegistrationAdmin(admin.ModelAdmin):
    list_display = ['member', 'pt_program', 'trainer', 'total_sessions', 'remaining_sessions', 'registration_status', 'registration_date']
    list_filter = ['registration_status', 'registration_date', 'pt_program']
    search_fields = ['member__name', 'pt_program__name', 'trainer__name']
    ordering = ['-registration_date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('등록 정보', {
            'fields': ('member', 'pt_program', 'trainer')
        }),
        ('PT 정보', {
            'fields': ('total_sessions', 'remaining_sessions', 'total_price', 'paid_amount')
        }),
        ('상태', {
            'fields': ('registration_status', 'registration_date', 'expiry_date')
        }),
        ('메모', {
            'fields': ('notes',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def branch(self, obj):
        return obj.member.branch.name
    branch.short_description = '지점'
