from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('info/', info, name='info'),
    path('ext-resources/', external_resources, name='ext_resources'),
    path('add_task/',
         RequestCreateView.as_view(model=Task, form_class=AddTaskForm, success_url=reverse_lazy('home'), template_name='forum/add_task.html',  success_message='Задача сохранена.'),
         name='add_task'),
    path('<slug:category_slug>/', TaskList.as_view(), name='category_detail'),
    path('<slug:category_slug>/task<int:task_id>', TaskDetail.as_view(), name='task_detail'),
    # path('<slug:category_slug>/task<int:task_id>/add-solution', RequestModelForm.as_view(), name='add_solution'),
    # path('<slug:category_slug>/task<int:task_id>/solution<int:solution_id>/add-comment', RequestModelForm.as_view(), name='add_comment')
]