from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from .forms import *
from .models import *


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


class UserLogin(LoginView):
    template_name = 'account/login.html'


class UserLogout(LogoutView):
    template_name = 'account/logout.html'

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


class UserPasswordChange(PasswordChangeView):
    template_name = 'account/registration/password_change_form.html'


class UserPasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/registration/password_change_done.html'


class UserPasswordReset(PasswordResetView):
    template_name = 'account/registration/password_reset_form.html'


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'account/registration/password_reset_done.html'


class UserPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'account/registration/password_reset_complete.html'


class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'account/registration/password_reset_confirm.html'


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        print(user_form)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # Создание профиля пользователя.
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/registration/register_done.html',
                          {'new_user': new_user})
        else:
            return HttpResponse(u'Куда прёшь?')
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/registration/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'forum/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})
