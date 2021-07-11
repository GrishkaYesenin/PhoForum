from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('info/', info, name='info'),
    path('ext-resources/', external_resources, name='ext_resources'),
    path('login/', index, name='login'),
    path('regin/', index, name='regin'),
    path('addtask/', addtask, name='addtask'),
    path('<slug:category_slug>/', category_detail, name='category_detail'),
    path('<slug:category_slug>/<int:task_id>', task_detail, name='task_detail')
]