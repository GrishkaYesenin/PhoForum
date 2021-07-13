from django.db import models
from django.conf import settings

# 1. Task
# 2. Comment
# 3. Category

from django.urls import reverse
from difflib import SequenceMatcher as SM

GRADE_CHOICES = (
    (7, "7"),
    (8, "8"),
    (9, "9"),
    (10, "10"),
    (11, "11"),
)


class SimilarTaskManager(models.Manager):
    def get(self, selected_task):
        '''Returns list of simmilar tasks to selected'''
        tasks = self.model.objects.all()
        result = []
        for task in tasks:
            if SM(None, task.content, selected_task.content).ratio() >= 0.7: # Мб стоит подобрать более оптимальный порог
                result.append(task)
        return result


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название задачи", blank=True)
    content = models.TextField(max_length=3500, verbose_name="Условие задачи")
    image = models.ImageField(blank=True, null=True, verbose_name="Рисунок к условию")
    resource = models.CharField(max_length=500, blank=True, verbose_name="Источник/название олимпиады")
    year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Год")
    grade = models.IntegerField(verbose_name="Класс",  choices=GRADE_CHOICES, default=None, blank=True, null=True)
    difficulty_level = models.PositiveSmallIntegerField(verbose_name="Уровень сложности", blank=True, null=True)
    answer = models.CharField(max_length=500, blank=True, verbose_name="Ответ")
    category = models.ForeignKey(
        'Category',
        verbose_name="Раздел",
        related_name='tasks',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    
    objects = models.Manager()
    similar = SimilarTaskManager()

    def __str__(self):
        return str(self.content)

    @property
    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'category_slug': self.category.slug, 'task_id': self.id})


    @property
    def get_name(self):
        name = ""
        if self.resource:
            name += self.resource + " "
        if self.grade:
            name += str(self.grade) + "кл. "
        if self.year:
            name += str(self.year) + "г."
        if name:
            name = f'({name})'
        return name

    class Meta:
        ordering = ['difficulty_level', 'grade', 'year']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    parent_category = models.ForeignKey('ParentCategory',  verbose_name="Категория из раздела", related_name='children_cat', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    @property
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})

    @property
    def get_num_task_by_cat(self):
        return len(Task.objects.filter(category_id=self.id))

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class ParentCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название раздела")

    def __str__(self):
        return str(self.name)

    @property
    def get_categories_by_parent(self):
        return Category.objects.filter(parent_category=self.id)

    class Meta:
        verbose_name_plural = "Parent Categories"


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительский комментарий",
        blank=True, null=True,
        related_name='comment_children',
        on_delete=models.CASCADE
    )
    is_child = models.BooleanField(default=False)
    solution = models.ForeignKey('Solution',  related_name='comments', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.text)

    class Meta:
        ordering = ['likes', 'created']

class Solution(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    voices = models.PositiveIntegerField(blank=True, null=True)
    task = models.ForeignKey(Task, related_name='solutions', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.body[:20])

    class Meta:
        ordering = ['voices']


