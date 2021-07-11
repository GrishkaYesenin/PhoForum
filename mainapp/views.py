from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .utils import create_comment_tree
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

ADD_PAGINATION = True


NUM_TASKS_ON_THE_PAGE = 4

EXTERNAL_RESOURCES = {
    'Math us!': 'https://mathus.ru/',
    'Сборник М.Ю. Замятнина 7-8кл': 'http://karand.ru/index.php?productID=1496',
    'Сливы Фоксфорда': 'https://github.com/limitedeternity/foxford_courses'
}


CATEGORY_MENU = {'p_categories': ParentCategory.objects.all(), 'categories': Category.objects.all()}


def index(request):
    context = {
        'p_categories': CATEGORY_MENU['p_categories'],
        'categories': CATEGORY_MENU['categories'],
        'title': 'PhoForum',
    }
    return render(request, 'mainapp/home.html', context=context)


def category_detail(request, category_slug):
    cat_by_slug = get_object_or_404(Category, slug=category_slug)
    task_list = cat_by_slug.tasks.all()
    paginator = Paginator(task_list, NUM_TASKS_ON_THE_PAGE)
    curr_page = request.GET.get('page')
    try:
        tasks = paginator.page(curr_page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    context = {
        'p_categories': CATEGORY_MENU['p_categories'],
        'categories': CATEGORY_MENU['categories'],
        'title': cat_by_slug,
        'category': cat_by_slug,
        'curr_page': curr_page,
        'tasks': tasks,
    }
    return render(request, 'mainapp/cat_detail.html', context=context)


def task_detail(request, category_slug, task_id):
    task_by_id = get_object_or_404(Task, id=task_id)
    if task_by_id.category.slug == category_slug:
        comments = task_by_id.comments.all()
        new_comment = None
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.task = task_by_id
                new_comment.save()
        else:
            comment_form = CommentForm()
        context = {
            'p_categories': CATEGORY_MENU['p_categories'],
            'categories': CATEGORY_MENU['categories'],
            'title': 'PhoForum',
            'task': task_by_id,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        }
    else:
        raise Http404("Invalid path.")
    return render(request, template_name='mainapp/task_detail.html', context=context)


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
