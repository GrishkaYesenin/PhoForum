from django.shortcuts import render
from .models import *


menu = ["O сайте", "Выбрать раздел", "Войти"]

def index(request):
    context = {'title': 'PhoForum', 'menu': menu}
    return render(request, 'mainapp/homepage.html', context)


def tasks(request, category_slug):
    context = {'title': 'PhoForum', 'category': category_slug}
    return render(request, 'mainapp/tasks.html', context)


def pageNotFound(request, exeption):
    return render(request, 'mainapp/404.html')