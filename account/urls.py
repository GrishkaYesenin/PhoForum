from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('password_change/', UserPasswordChange.as_view(), name='password_change'),
    path('password_change/done/', UserPasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', UserPasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/done/', UserPasswordResetComplete.as_view(), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit')
]