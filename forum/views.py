from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView

from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView, DetailView

ADD_PAGINATION = True

NUM_TASKS_ON_THE_PAGE = 4

EXTERNAL_RESOURCES = {
    'Math us!': 'https://mathus.ru/',
    'Сборник М.Ю. Замятнина 7-8кл': 'http://karand.ru/index.php?productID=1496',
    'Сливы Фоксфорда': 'https://github.com/limitedeternity/foxford_courses'
}


def index(request):
    return render(request, 'forum/home.html', {'title': 'PhoForum'})


def info(request):
    return render(request, 'forum/info.html')


def external_resources(request):
    return render(request, 'forum/external_resources.html', context=EXTERNAL_RESOURCES)


class TaskList(ListView):
    context_object_name = 'tasks'
    template_name = 'forum/category/cat_detail.html'
    paginate_by = 4

    def get_queryset(self):
        cat_slug = self.kwargs['category_slug']
        if cat_slug == 'vse-razdely':
            self.category = 'Все разделы'
            task_list = Task.objects.all()
        else:
            self.category = get_object_or_404(Category, slug=cat_slug)
            task_list = self.category.tasks.all()
        return task_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = self.category
        context['category'] = self.category
        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'forum/category/task_detail.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Task, id=self.kwargs['task_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['category_slug']
        context['category'] = self.get_object().category
        context['solutions'] = self.get_object().solutions.all()
        context['solution_form'] = SolutionForm()
        context['comment_form'] = CommentForm()
        return context


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


class RequestCreateView(SuccessMessageMixin, CreateView):
    """ 
    Sub-class of the CreateView to automatically pass the Request to the Form. 
    """
    success_message = "Created Successfully"

    # def get_form_kwargs(self):
    #     """ Add the Request object to the Form's Keyword Arguments. """
    #     kwargs = super(RequestCreateView, self).get_form_kwargs()
    #     kwargs.update({'request': self.request})
    #     return kwargs


class RequestUpdateView(SuccessMessageMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.        
    """
    success_message = "Updated Successfully"

    def get_form_kwargs(self):
        """ Add the Request object to the form's keyword arguments. """
        kwargs = super(RequestUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        qs = super(RequestUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class RequestDeleteView(SuccessMessageMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other 
    user's data.
    """
    success_message = "Deleted Successfully"

    def get_queryset(self):
        qs = super(RequestDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


