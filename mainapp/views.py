from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

ADD_PAGINATION = True


NUM_TASKS_ON_THE_PAGE = 4

EXTERNAL_RESOURCES = {
    'Math us!': 'https://mathus.ru/',
    'Сборник М.Ю. Замятнина 7-8кл': 'http://karand.ru/index.php?productID=1496',
    'Сливы Фоксфорда': 'https://github.com/limitedeternity/foxford_courses'
}




def index(request):
    context = {
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
        start_index_on_curr_page = (curr_page - 1) * NUM_TASKS_ON_THE_PAGE + 1
    except PageNotAnInteger:
        tasks = paginator.page(1)
        start_index_on_curr_page = 1
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
        start_index_on_curr_page = 1
    context = {
        'title': cat_by_slug,
        'category': cat_by_slug,
        'curr_page': curr_page,
        'tasks': tasks,
        'start_index_on_curr_page': start_index_on_curr_page,
    }
    return render(request, 'mainapp/cat_detail.html', context=context)


def task_detail(request, category_slug, task_id):
    task_by_id = get_object_or_404(Task, id=task_id)
    if task_by_id.category.slug == category_slug:
        solutions = task_by_id.solutions.all()
        context = {
            'title': 'PhoForum',
            'task': task_by_id,
            'solutions': solutions,
        }
    else:
        raise Http404("Invalid path.")
    solution_context = create_solution(request, task_id)
    # comment_context = create_comment(request, solution_id)
    context = {**context, **solution_context}
    return render(request, template_name='mainapp/task_detail.html', context=context)


def create_solution(request, task_id):
    new_solution = None
    if request.method == 'POST':
        solution_form = SolutionForm(request.POST, request.FILES)
        if solution_form.is_valid():
            new_solution = solution_form.save(commit=False)
            new_solution.task = get_object_or_404(Task, id=task_id)
            new_solution.save()
    else:
        solution_form = SolutionForm()
    context = {
        'new_solution': new_solution,
        'solution_form': solution_form
        }
    return context


def create_comment(request, solution_id):
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.solution = get_object_or_404(Solution, id=solution_id)
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'new_comment': new_comment,
        'comment_form': comment_form
        }
    return context


def add_task(request):
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
        return render(request, 'mainapp/add_task.html', context=context)


def info(request):
    return render(request, 'mainapp/info.html')


def external_resources(request):
    return render(request, 'mainapp/external_resources.html', context=EXTERNAL_RESOURCES)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'mainapp/login.html', {'form': form})