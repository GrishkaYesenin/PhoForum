from django.contrib import admin

from .models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ['content', 'resource', 'difficulty_level', 'answer', 'chat', 'category']
    list_display_links = ['content']
    search_fields = ['content']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Chat)
admin.site.register(Comment)

