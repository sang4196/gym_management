from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Branch, BranchAdmin


@admin.register(Branch)
class BranchModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'phone', 'email', 'address']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'address', 'phone', 'email')
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BranchAdmin)
class BranchAdminUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'admin_type', 'branch', 'is_active', 'date_joined']
    list_filter = ['admin_type', 'is_active', 'date_joined', 'branch']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['username']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('개인 정보', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('권한', {
            'fields': ('admin_type', 'branch', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('중요한 날짜', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'admin_type', 'branch', 'is_active'),
        }),
    )
