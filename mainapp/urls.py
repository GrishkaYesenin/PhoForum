from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='base'),
    path('info/', info, name='info'),
    path('ext-resources/', external_resources, name='ext_resources'),
    path('login/', user_login, name='login'),
    path('regin/', index, name='regin'),
    path('add_task/', add_task, name='add_task'),
    path('<slug:category_slug>/', category_detail, name='category_detail'),
    path('<slug:category_slug>/task<int:task_id>', task_detail, name='task_detail'),
    # path('<slug:category_slug>/task<int:task_id>/add_solution', add_solution, name='add_solution'),
    # path('<slug:category_slug>/task<int:task_id>/solution<int:solution_id>/add_comment', add_comment, name='add_comment')
]