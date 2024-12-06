from django.db import models
from django.contrib.auth.models import User

class UnripeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.CharField(max_length=200, null=True)

class Movie(models.Model):
    poster = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    genre = models.CharField(max_length=200, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    runtime = models.CharField(max_length=15, null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=1000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    type = models.CharField(max_length=200)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()