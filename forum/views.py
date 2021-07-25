from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import *

from django.views.generic import ListView, DetailView


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
        context['url'] = self.get_object().get_absolute_url
        context['curr_user'] = self.request.session.get('user')
        context['solution_form'] = SolutionForm()
        context['comment_form'] = CommentForm()
        return context


class RequestCreateView(SuccessMessageMixin, CreateView):
    """ 
    Sub-class of the CreateView to automatically pass the Request to the Form. 
    """
    success_message = "Created Successfully"

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'category_slug': self.kwargs["category_slug"], 'task_id': self.kwargs["task_id"]})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_value'] = "Update"


class RequestDeleteView(SuccessMessageMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other 
    user's data.
    """
    success_message = "Deleted Successfully"

    def get_queryset(self):
        qs = super(RequestDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_value'] = "Confirm"


class TaskCreateView(CreateView):
    form_class = AddTaskForm
    success_url = reverse_lazy('home')
    template_name = 'forum/add_task.html'


class SolutionCreateView(RequestCreateView):
    form_class = SolutionForm
    template_name = 'forum/category/forms/solution_form.html'

    # def get_success_url(self):
    #     return reverse_lazy('task_detail', kwargs={'category_slug': self.kwargs["category_slug"], 'task_id': self.kwargs["task_id"]})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task = get_object_or_404(Task, id=self.kwargs["task_id"])
        return super().form_valid(form)


class SolutionUpdateView(RequestUpdateView):
    form_class = SolutionForm
    template_name = 'forum/category/forms/solution_form.html'


class SolutionDeleteView(RequestDeleteView):
    form_class = SolutionForm
    template_name = 'forum/category/forms/solution_form.html'


class CommentCreateView(RequestCreateView):
    form_class = CommentForm
    template_name = 'forum/category/forms/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.solution = get_object_or_404(Solution, id=self.kwargs["solution_id"])
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('task_detail', kwargs={'category_slug': self.kwargs["category_slug"], 'task_id': self.kwargs["task_id"]})


class CommentUpdateView(RequestUpdateView):
    form_class = CommentForm
    template_name = 'forum/category/forms/comment_form.html'


class CommentDeleteView(RequestDeleteView):
    form_class = CommentForm
    template_name = 'forum/category/forms/comment_form.html'