from django.contrib import admin
from django import forms

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
    list_display = ['author', 'text', 'created', 'updated']
    list_display_links = ['text']
    search_fields = ['author']

class SolutionAdmin(admin.ModelAdmin):
    list_display = ['author', 'body', 'created', 'updated']
    list_display_links = ['body']
    search_fields = ['author']



admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(ParentCategory)

