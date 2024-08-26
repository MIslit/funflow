from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-time_create']
        
    def get_absolute_url(self):
        return reverse("idea", kwargs={"idea_id": self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Score(models.IntegerChoices):
        УЖАСНО = 1
        ПЛОХО = 2
        НОРМАЛЬНО = 3
        ХОРОШО = 4
        ОТЛИЧНО = 5
    
    class Meta:
        ordering = ['-time_create']
    
    score = models.IntegerField(choices=Score.choices)
    text = models.TextField(blank=False)
    time_create = models.DateTimeField(auto_now_add=True)
    idea = models.ForeignKey('Idea', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
