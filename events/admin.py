from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'location', 'price', 'is_active', 'is_featured']
    list_filter = ['event_type', 'is_active', 'is_featured', 'start_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_active', 'is_featured']
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'short_description', 'event_type')
        }),
        ('Дата та місце', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('Ціна та учасники', {
            'fields': ('price', 'max_participants', 'current_participants')
        }),
        ('Статус та зображення', {
            'fields': ('is_active', 'is_featured', 'image')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
