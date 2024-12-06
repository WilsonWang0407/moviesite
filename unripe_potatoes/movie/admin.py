from django.contrib import admin
from movie.models import Movie, Rating, Feedback, Comment

@admin.register(Movie)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'genre')

@admin.register(Rating)
class PageAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating')

@admin.register(Comment)
class PageAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'comment')

@admin.register(Feedback)
class PageAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'message')