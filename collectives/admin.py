from django.contrib import admin
from .models import Collective, CollectiveRegistration, Review

@admin.register(Collective)
class CollectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'collective_type', 'age_group', 'leader', 'is_active']
    list_filter = ['collective_type', 'age_group', 'is_active']
    search_fields = ['name', 'description', 'leader']
    list_editable = ['is_active']
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'collective_type', 'age_group', 'description', 'short_description')
        }),
        ('Керівник', {
            'fields': ('leader', 'leader_photo', 'leader_description')
        }),
        ('Розклад та ціни', {
            'fields': ('schedule',)
        }),
        ('Додатково', {
            'fields': ('is_active', 'image', 'youtube_url', 'rating')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

@admin.register(CollectiveRegistration)
class CollectiveRegistrationAdmin(admin.ModelAdmin):
    list_display = ['child_name', 'collective', 'parent_name', 'phone', 'status', 'created_at']
    list_filter = ['status', 'collective', 'created_at']
    search_fields = ['child_name', 'parent_name', 'phone', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'collective', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'collective']
    search_fields = ['author_name', 'content']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
