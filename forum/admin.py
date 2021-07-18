from django.contrib import admin

from .models import *


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['content', 'resource', 'answer', 'category', 'image', 'year', 'grade']
    list_display_links = ['content']
    list_editable = ['resource', 'answer', 'category', 'year', 'grade']
    search_fields = ['content', 'category', 'resource']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name']
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'created', 'updated']
    list_display_links = ['text']
    search_fields = ['author']


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['author', 'body', 'created', 'updated']
    list_display_links = ['body']
    search_fields = ['author']


admin.site.register(ParentCategory)

