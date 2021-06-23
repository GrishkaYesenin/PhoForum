from django.shortcuts import render
from .models import *


menu = ["O сайте", "Выбрать раздел", "Войти"]

def index(request):
    categories = Category.objects.all()
    context = {
        'title': 'PhoForum',
        'menu': menu,
        'categories': categories
    }
    return render(request, 'mainapp/homepage.html', context=context)


def get_list_of_tasks(request, category_slug):
    cat_by_slug, = Category.objects.filter(slug=category_slug)
    if cat_by_slug:
         template_name = 'mainapp/category.html'
         tasks = Task.objects.filter(category=cat_by_slug.id)
         context = {
             'title': 'PhoForum',
             'category': category_slug,
             'tasks': tasks
         }
    else:
        template_name =  'mainapp/404.html'
        context = {'text_exeption': "Такой категории нет"} #сделать вызов функции pageNotFound

    return render(request, template_name=template_name, context=context)


def get_task(request, category_slug, task_id):
    context = {
        'title': 'PhoForum',
        'category': category_slug,
        'task_id': task_id
    }
    task_by_id, = Task.objects.filter(id=task_id)
    if task_by_id and task_by_id.category.slug == category_slug:
        task = Task.objects.get(task_id)
        context['task'] = task
        template_name = 'mainapp/task.html'
    else:
        template_name = 'mainapp/404.html'
        context = {'text_exeption': "Такой категории нет"}  # сделать вызов функции pageNotFound

    return render(request, template_name=template_name, context=context)


def pageNotFound(request, exeption):
    return render(request, 'mainapp/404.html')