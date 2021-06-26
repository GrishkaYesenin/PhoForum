from django.contrib import admin

from .models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ['content', 'resource', 'difficulty_level', 'answer', 'category', 'image']
    list_display_links = ['content']
    search_fields = ['content']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name']
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)

