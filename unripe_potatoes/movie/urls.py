from django.urls import path
from django.conf.urls import handler404

from movie import views

app_name = 'movie'

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/all', views.all_movies, name='all_movies'),
    path('movies/<str:genre>', views.genre_movies, name='genre'),
    path('movie/<int:id>', views.movie, name='movie'),
    path('search/<str:q>', views.search_movie, name='search'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('register', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('handle-favorite/', views.handle_favorite, name='handle_favorite'),
    path('feedback', views.feedback, name='feedback'),
    path('feedback-success/', views.feedback_success, name='feedback_success'),
    path('add-rating/', views.add_rating, name='add_rating'),
    path('favorite/', views.favorite_movies, name='favorute'),
]

handler404 = views.page_404