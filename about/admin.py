from django.contrib import admin
from .models import HistoryTimeline, TeamMember, ContactInfo, ContactFormSubmission, Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'order', 'is_active', 'get_member_count']
    list_filter = ['department', 'is_active']
    search_fields = ['name']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'department')
        }),
        ('Додаткові налаштування', {
            'fields': ('order', 'is_active')
        }),
    )

    def get_member_count(self, obj):
        return obj.team_members.count()

    get_member_count.short_description = 'Кількість співробітників'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_position', 'get_department', 'is_active', 'order']
    list_filter = ['position__department', 'is_active']
    search_fields = ['name', 'bio', 'position__name']
    list_editable = ['is_active', 'order']
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'nickname', 'position', 'bio', 'short_bio', 'photo', 'slug')
        }),
        ('Контактна інформація', {
            'fields': ('email', 'phone')
        }),
        ('Додаткові налаштування', {
            'fields': ('is_active', 'order')
        }),
    )

    def get_position(self, obj):
        return obj.position.name

    get_position.short_description = 'Посада'

    def get_department(self, obj):
        return obj.position.get_department_display()

    get_department.short_description = 'Відділ'


@admin.register(HistoryTimeline)
class HistoryTimelineAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'is_important', 'order', 'created_at']
    list_filter = ['year', 'is_important', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_important', 'order']
    fieldsets = (
        ('Основна інформація', {
            'fields': ('year', 'title', 'description', 'image')
        }),
        ('Додаткові налаштування', {
            'fields': ('is_important', 'order')
        }),
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Дозволяємо створення тільки якщо записів ще немає
        return not ContactInfo.objects.exists()

    fieldsets = (
        ('Контактна інформація', {
            'fields': ('address', 'phone', 'email', 'work_hours')
        }),
        ('Карта', {
            'fields': ('map_embed_code', 'latitude', 'longitude')
        }),
        ('Соціальні мережі', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'telegram_url')
        }),
    )

@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_processed', 'created_at']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_processed']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Інформація про відправника', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Повідомлення', {
            'fields': ('subject', 'message')
        }),
        ('Статус', {
            'fields': ('is_processed', 'created_at')
        }),
    )
