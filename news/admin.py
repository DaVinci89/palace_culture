from django.contrib import admin
from .models import News, Tag, Comment, GalleryCategory, GalleryImage


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at', 'tags']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'slug', 'short_content', 'content', 'image', 'tags')
        }),
        ('Публікація', {
            'fields': ('is_published',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'news', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author__username', 'content', 'news__title']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']



