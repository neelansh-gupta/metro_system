from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model."""
    
    list_display = ('username', 'email', 'user_type', 'balance', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Metro System', {
            'fields': ('user_type', 'phone_number', 'balance'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Metro System', {
            'fields': ('user_type', 'phone_number'),
        }),
    )
