from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView


ADD_PAGINATION = True


NUM_TASKS_ON_THE_PAGE = 4

EXTERNAL_RESOURCES = {
    'Math us!': 'https://mathus.ru/',
    'Сборник М.Ю. Замятнина 7-8кл': 'http://karand.ru/index.php?productID=1496',
    'Сливы Фоксфорда': 'https://github.com/limitedeternity/foxford_courses'
}

class TaskList(ListView):
    context_object_name = 'tasks'
    template_name = 'forum/category/cat_detail.html'

    def get_queryset(self, **kwargs):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return self.category.tasks.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['category_slug']
        context['category'] = self.category
        return context



def index(request):
    return render(request, 'forum/home.html', {'title': 'PhoForum'})


def category_detail(request, category_slug):
    cat_by_slug = get_object_or_404(Category, slug=category_slug)
    task_list = cat_by_slug.tasks.all()
    paginator = Paginator(task_list, NUM_TASKS_ON_THE_PAGE)
    curr_page = request.GET.get('page')
    try:
        tasks = paginator.page(curr_page)
        start_index_on_curr_page = (int(curr_page)-1)*NUM_TASKS_ON_THE_PAGE
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
    return render(request, 'forum/category/cat_detail.html', context=context)


# class TaskDetail(ListView):
#     context_object_name = 'solutions'
#     template_name='forum/task_detail.html'
#
#     def get_queryset(self, **kwargs):
#         return get_object_or_404(Task, id=self.kwargs['task_id'])
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         context['title'] = self.kwargs['category_slug']
#         context['category'] = self.category
#         return context

def task_detail(request, category_slug, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.category.slug == category_slug:
        solutions = task.solutions.all()
        context = {
            'title': 'PhoForum',
            'task': task,
            'solutions': solutions,
            'category_slug': category_slug,
            'task_id': task_id
        }
    else:
        raise Http404("Invalid path.")

    solution_form = SolutionForm()
    comment_form = CommentForm()
    form_context = {
        'solution_form': solution_form,
        'comment_form': comment_form,
    }
    context = {**context, **form_context}
    return render(request, template_name='forum/category/task_detail.html', context=context)


def add_solution(request, category_slug, task_id):
    if request.method == 'POST':
        solution_form = SolutionForm(request.POST, request.FILES)
        if solution_form.is_valid():
            new_solution = solution_form.save(commit=False)
            new_solution.task = get_object_or_404(Task, id=task_id)
            new_solution.save()
            return redirect('task_detail', category_slug=category_slug, task_id=task_id)


def add_comment(request, category_slug, task_id, solution_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.solution = get_object_or_404(Solution, id=solution_id)
            new_comment.save()
            return redirect('task_detail', category_slug=category_slug, task_id=task_id)


def add_task(request):
    new_task = None
    if request.method == 'POST':
        task_form = AddTaskForm(request.POST, request.FILES)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.save()
            return redirect('home')
    else:
        task_form = AddTaskForm()
        context = {
            'title': 'PhoForum',
            'new_task': new_task,
            'form': task_form,
        }
        return render(request, 'forum/add_task.html', context=context)


def info(request):
    return render(request, 'forum/info.html')


def external_resources(request):
    return render(request, 'forum/external_resources.html', context=EXTERNAL_RESOURCES)