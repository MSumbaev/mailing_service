from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'view_count', 'published_at', )
    list_filter = ('view_count', 'published_at', )
    search_fields = ('title', 'content', 'published_at', )
