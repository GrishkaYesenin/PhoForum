from django.db import models
from django.conf import settings

# 1. Problem
# 2. Catalog
# 3. Comment
# 4. User
# 5. Categori
# 6. Chat

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE)
    text = models.TextField(max_length=1500)
    timestamp_create = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(null=True)
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительский комментарий",
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE

    )

    # class Meta:
    #     ordering = [likes]
    #     ordering = [timestamp]

    def __str__(self):
        return "Message text"


class Chat(models.Model):
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return "Chat"



class Task(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100, verbose_name="Название задачи")
    content = models.TextField(max_length=1500, verbose_name="Условие задачи")
    image = models.ImageField()
    resource = models.CharField(max_length=500, blank=True)
    grade = models.PositiveSmallIntegerField(verbose_name="Класс", blank=True)
    difficulty_level = models.PositiveSmallIntegerField(verbose_name="Уровень сложности", blank=True, null=True)
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.title)


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100, verbose_name="Название раздела")
    tasks_by_category = models.ForeignKey(Task, verbose_name="Задачи данной категории", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Catalog(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = [Task.'difficulty_level']

    def __str__(self):
        return "Catalog"




