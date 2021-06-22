from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('<slug:category_slug>/', get_list_of_tasks, name='category'),
    path('<slug:category_slug>/<int:task_id>', get_task)
]