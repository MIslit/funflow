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
        return reverse("idea", kwargs={"idea_id": self.id})

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Score(models.IntegerChoices):
        VERY_BAD = 1
        BAD = 2
        NORMAL = 3
        GOOD = 4
        PERFECT = 5
    
    class Meta:
        ordering = ['-time_create']
    
    score = models.IntegerField(choices=Score.choices)
    text = models.TextField(blank=False)
    time_create = models.DateTimeField(auto_now_add=True)
    idea = models.ForeignKey('Idea', null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

# class Rating(models.Model):
#     class Score(models.IntegerChoices):
#         VERY_BAD = 1
#         BAD = 2
#         NORMAL = 3
#         GOOD = 4
#         PERFECT = 5

#     score = models.IntegerField(choices=Score.choices)
#     time_create = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     idea = models.ForeignKey('Idea', null=True, on_delete=models.SET_NULL)
    
#     def __str__(self):
#         return str(self.pk)