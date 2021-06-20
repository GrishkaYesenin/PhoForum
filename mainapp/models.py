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
    text = models.TextField(max_length=1500, help_text="Message text")
    data = models.DateField(auto_now=True, verbose_name="Дата создания комментария")
    timestamp = models.DateTimeField(auto_now=True)
    likes = models.PositiveSmallIntegerField(null=True)
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительский комментарий",
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE

    )
    object_id = models.PositiveIntegerField()

    # class Meta:
    #     ordering = [likes]
    #     ordering = [timestamp]

    def __str__(self):
        return "Message text"


class Chat(models.Model):
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return "Chat"


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100, verbose_name="Название раздела")
    tasks_by_category = models.ForeignKey(Task, blank=True, verbose_name="Задачи данной категории", related_name="relared_tasks_by_category")

    def __str__(self):
        return str(self.name)


class Task(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100, verbose_name="Название задачи")
    content = models.TextField(max_length=1500, verbose_name="Условие задачи")
    image = models.ImageField()
    resource = models.CharField(max_length=500)
    grade = models.PositiveSmallIntegerField(verbose_name="Класс")
    difficulty_level = models.PositiveSmallIntegerField(verbose_name="Уровень сложности")

    # categori = models.ForeignKey(Category, verbose_name="Раздел", related_name="related_")
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.title)


class Catalog(models.Model):
    slug = models.SlugField()
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = [Task.'difficulty_level']

    def __str__(self):
        return "Catalog"




