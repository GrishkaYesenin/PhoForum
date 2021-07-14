from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('info/', info, name='info'),
    path('ext-resources/', external_resources, name='ext_resources'),
    path('add_task/', add_task, name='add_task'),
    path('<slug:category_slug>/', category_detail, name='category_detail'),
    path('<slug:category_slug>/task<int:task_id>', task_detail, name='task_detail'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
]