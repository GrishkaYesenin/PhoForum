from django.contrib import admin

from .models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ['content', 'resource', 'answer', 'category', 'image']
    list_display_links = ['content']
    search_fields = ['content', 'category', 'resource']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name']
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']
    list_display_links = ['text']
    search_fields = ['author']
    date_hierarchy = 'timestamp_create'


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ParentCategory)

