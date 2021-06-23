from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('info/', index, name='info'),
    path('recources/', index, name='recources'),
    path('login/', index, name='login'),
    path('regin/', index, name='regin'),
    path('<slug:category_slug>/', get_list_of_tasks, name='category'),
    path('<slug:category_slug>/<int:task_id>', get_task, name='task')
]