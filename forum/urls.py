from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('info/', info, name='info'),
    path('ext-resources/', external_resources, name='ext_resources'),
    path('add_task/', TaskCreateView.as_view(), name='add_task'),
    path('<slug:category_slug>/', TaskList.as_view(), name='category_detail'),
    path('<slug:category_slug>/task<int:task_id>', TaskDetail.as_view(), name='task_detail'),
    path('<slug:category_slug>/task<int:task_id>/add-solution', SolutionCreateView.as_view(), name='add_solution'),
    # path('<slug:category_slug>/task<int:task_id>/solution<int:solution_id>', SolutionUpdateView.as_view(), name='edit_solution'),
    # path('<slug:category_slug>/task<int:task_id>/solution<int:solution_id>/delete', SolutionDeleteView.as_view(), name='delete_solution'),
    path('<slug:category_slug>/task<int:task_id>/solution<int:solution_id>/add-comment', CommentCreateView.as_view(), name='add_comment')
]