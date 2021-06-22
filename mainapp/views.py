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
    context = {
        'title': 'PhoForum',
        'category': category_slug
    }
    if category_slug in [elem.slug for elem in Category.objects.all()]:
        return render(request, 'mainapp/category.html', context=context)
    else:
        return render(request, 'mainapp/404.html', {'text_exeption': "Такой категории нет"}) #сделать вызов функции pageNotFound


def get_task(request, category_slug, task_id):
    context = {
        'title': 'PhoForum',
        'category': category_slug,
        'task_id': task_id
    }
    if category_slug in [elem.slug for elem in Category.objects.all()] and\
    task_id in [elem.tasks_by_category for elem in Category.objects.filter(slug=category_slug)]:
        task = Task.objects.get(task_id)
        context['task'] = task
        return render(request, 'mainapp/task.html', context=context)
    else:
        return render(request, 'mainapp/404.html', {'text_exeption': "Такой категории нет"}) #сделать вызов функции pageNotFound


def pageNotFound(request, exeption):
    return render(request, 'mainapp/404.html')