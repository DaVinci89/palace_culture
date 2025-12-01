from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'full_name', 'is_staff', 'email_confirmed', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'email_confirmed', 'date_joined', 'email_notifications']
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined', 'created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Персональна інформація'), {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'avatar', 'bio', 'website')
        }),
        (_('Дозволи'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Важливі дати'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
        (_('Налаштування сповіщень'), {
            'fields': ('email_notifications', 'sms_notifications', 'email_confirmed')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = _('Повне ім\'я')