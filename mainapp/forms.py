from django import forms
from .models import *
from django.contrib.auth.models import User

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'image', 'resource', 'year', 'grade', 'category', 'answer']

    def save(self, commit=True):
        task = super(AddTaskForm, self).save(commit=False)
        if commit:
            similar = Task.similar.get(task)
            print(similar)
            if similar:
                print(similar)
                raise Exception("Task is very simmilar") #TODO Shoow error msg to user
        super().save()
        return task

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['author', 'body']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']