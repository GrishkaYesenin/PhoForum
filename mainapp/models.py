from django.db import models
from django.conf import settings

# 1. Task
# 3. Comment
# 5. Category
# 6. Chat
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название задачи")
    content = models.TextField(max_length=1500, verbose_name="Условие задачи")
    image = models.ImageField(blank=True, null=True)
    resource = models.CharField(max_length=500, blank=True)
    grade = models.PositiveSmallIntegerField(verbose_name="Класс", blank=True, null=True)
    difficulty_level = models.PositiveSmallIntegerField(verbose_name="Уровень сложности", blank=True, null=True)
    chat = models.OneToOneField('Chat', on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        verbose_name="Задачи данной категории",
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('category', kwargs={'task_id': self.id})


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название раздела")

    def __str__(self):
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('home', kwargs={'category_slug': self.slug})


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE)
    text = models.TextField(max_length=1500)
    timestamp_create = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(null=True)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительский комментарий",
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE

    )

    def __str__(self):
        return "Message text"


class Chat(models.Model):


    def __str__(self):
        return "Chat"
