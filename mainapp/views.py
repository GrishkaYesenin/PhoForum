from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    categories = Category.objects.all()
    context = {
        'title': 'PhoForum',
        'categories': categories
    }
    return render(request, 'mainapp/homepage.html', context=context)


def get_list_of_tasks(request, category_slug):
    cat_by_slug = get_object_or_404(Category, slug=category_slug)
    tasks = Task.objects.filter(category=cat_by_slug.id)
    context = {
         'title': 'PhoForum',
         'category': cat_by_slug,
         'tasks': tasks
    }
    return render(request, 'mainapp/category.html', context=context)


def get_task(request, category_slug, task_id):
    context = {
        'title': 'PhoForum',
        'category': category_slug,
        'task_id': task_id
    }
    task_by_id = Task.objects.get(id=task_id)
    if task_by_id and task_by_id.category.slug == category_slug:
        context['task'] = task_by_id
        template_name = 'mainapp/task.html'
    else:
        template_name = 'mainapp/404.html'
        context = {'text_exeption': "Такой категории нет"}  # сделать вызов функции pageNotFound

    return render(request, template_name=template_name, context=context)


def pageNotFound(request, exeption):
    return render(request, 'mainapp/404.html')