from django.contrib import admin
from .models import Reservation, PTRecord, PTRecordImage, ReservationChangeLog


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['member', 'trainer', 'date', 'start_time', 'duration', 'reservation_status', 'repeat_type']
    list_filter = ['reservation_status', 'repeat_type', 'date', 'trainer']
    search_fields = ['member__name', 'trainer__name', 'notes']
    ordering = ['-date', '-start_time']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('예약 정보', {
            'fields': ('member', 'trainer', 'pt_registration')
        }),
        ('일정', {
            'fields': ('date', 'start_time', 'end_time', 'duration')
        }),
        ('상태', {
            'fields': ('reservation_status',)
        }),
        ('반복', {
            'fields': ('repeat_type', 'repeat_end_date')
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


@admin.register(PTRecord)
class PTRecordAdmin(admin.ModelAdmin):
    list_display = ['member', 'trainer', 'workout_date', 'workout_time', 'duration', 'is_completed']
    list_filter = ['workout_date', 'is_completed', 'trainer']
    search_fields = ['member__name', 'trainer__name', 'content']
    ordering = ['-workout_date', '-workout_time']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('reservation', 'trainer', 'member')
        }),
        ('운동 정보', {
            'fields': ('workout_date', 'workout_time', 'duration', 'content')
        }),
        ('상태 및 메모', {
            'fields': ('member_condition', 'trainer_notes', 'is_completed')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def branch(self, obj):
        return obj.member.branch.name
    branch.short_description = '지점'


@admin.register(PTRecordImage)
class PTRecordImageAdmin(admin.ModelAdmin):
    list_display = ['pt_record', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['pt_record__member__name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('이미지 정보', {
            'fields': ('pt_record', 'image', 'description')
        }),
        ('생성일', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReservationChangeLog)
class ReservationChangeLogAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'change_type', 'changed_by', 'previous_status', 'new_status', 'created_at']
    list_filter = ['change_type', 'created_at']
    search_fields = ['reservation__member__name', 'changed_by', 'reason']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('변경 정보', {
            'fields': ('reservation', 'change_type', 'changed_by')
        }),
        ('상태 변경', {
            'fields': ('previous_status', 'new_status', 'reason')
        }),
        ('생성일', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
