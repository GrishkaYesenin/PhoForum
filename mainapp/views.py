from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .utils import create_comment_tree


EXTERNAL_RESOURCES = {
    'Math us!': 'https://mathus.ru/',
    'Сборник М.Ю. Замятнина 7-8кл': 'http://karand.ru/index.php?productID=1496',
    'Сливы Фоксфорда': 'https://github.com/limitedeternity/foxford_courses'
}


def index(request):
    parent_categories = ParentCategory.objects.all()
    context = {
        'title': 'PhoForum',
        'p_categories': parent_categories
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
    task_by_id = get_object_or_404(Task, id=task_id)
    if task_by_id.category.slug == category_slug:
        comments = Comment.objects.filter(task_id=task_id)
        tree = create_comment_tree(comments)
        context = {
            'title': 'PhoForum',
            'task': task_by_id,
            'tree': tree
        }
        template_name = 'mainapp/task.html'
    else:
        raise Http404("Invalid path.")

    return render(request, template_name=template_name, context=context)


def addtask(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddTaskForm()
    context = {
        'title': 'PhoForum',
        'form': form
    }
    return render(request, 'mainapp/addtask.html', context=context)


def info(request):
    return render(request, 'mainapp/info.html')


def external_resources(request):
    return render(request, 'mainapp/external_resources.html', context=EXTERNAL_RESOURCES)
