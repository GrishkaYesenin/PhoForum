from django import forms
from .models import *
import datetime
from django.views.generic import edit


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'image', 'resource', 'year', 'grade', 'category', 'answer']
    # 1962

    def clean_year(self):
        data = self.cleaned_data['year']
        if data > datetime.datetime.now().year:
            raise forms.ValidationError("You cannot set year more then current year.")
        if data < 1960:
            raise forms.ValidationError("You cannot set year low then 1960.")

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

