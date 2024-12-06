import json
import random

from django.contrib.auth.models import User
from movie.models import Movie, Favorite, Feedback, Comment, Rating

MENU_LINKS = {
    'all': 'All Movies',
    'action': 'Action Movies',
    'comedy': 'Comedy Movies',
    'fantasy': 'Fantasy Movies',
    'horror': 'Horror Movies',
    'thriller': 'Thriller Movies',
}

def get_random_movies(num):
    valid_movies_id_list = Movie.objects.all().values_list('id', flat=True)    
    random_movies_id_list = [random.choice(valid_movies_id_list) for _ in range(num)]    
    random_movies = Movie.objects.filter(id__in=random_movies_id_list)
    return random_movies

def get_movies_by_genre(genre, num):
    return Movie.objects.filter(genre__contains=genre)[:num]

def get_all_movies(user):
    movies = Movie.objects.values()
    all_movies = []
    for movie in movies:
        movie['rating'] = get_rating_by_movie_id(movie['id'])
        movie['favorite'] = check_user_favorite(movie['id'], user) if not user.username == '' else False
        movie['loggedIn'] = not user.username == ''
        all_movies.append(movie)
    return json.dumps(all_movies)

def get_fav_movies(user):
    movies = Favorite.objects.filter(user=user).values('movie')
    all_movies = []
    for movie_id in movies:
        movie = Movie.objects.filter(id=movie_id['movie']).values()[0]
        movie['rating'] = get_rating_by_movie_id(movie['id'])
        movie['favorite'] = check_user_favorite(movie['id'], user) if not user.username == '' else False
        movie['loggedIn'] = not user.username == ''
        all_movies.append(movie)
    return json.dumps(all_movies)

def get_genre_movies(genre, user):
    movies = Movie.objects.filter(genre__contains=genre).values()
    genre_movies = []
    for movie in movies:
        movie['rating'] = get_rating_by_movie_id(movie['id'])
        movie['favorite'] = check_user_favorite(movie['id'], user) if not user.username == '' else False
        movie['loggedIn'] = not user.username == ''
        genre_movies.append(movie)
    return json.dumps(genre_movies)

def get_movie_by_id(id):
    movie = Movie.objects.filter(id=id)[0]
    return movie

def search_movies_by_name(q):
    searches = Movie.objects.filter(name__icontains=q).values()
    return json.dumps(list(searches))

def search_suggestions_by_name(q):
    searches = {
        'names': list(Movie.objects.filter(name__icontains=q).values_list('name', flat=True)),
        'id': list(Movie.objects.filter(name__icontains=q).values_list('id', flat=True)),
    }
    return searches

def get_genre_list():
    genre_entries = [genre for genre in list(Movie.objects.values_list('genre', flat=True))]
    genre_list = []

    for genres in genre_entries:
        genre_list += str.split(genres, ', ')
    
    genre_list = list(set(genre_list))

    genre_list.sort()

    return genre_list

def get_fav_genre_list(user):
    movies = Favorite.objects.filter(user=user).values('movie')
    genre_list = []
    genre_entries = []
    for movie_id in movies:
        movie = Movie.objects.filter(id=movie_id['movie']).values()[0]
        genre_entries.append(movie['genre'])

    for genres in genre_entries:
        genre_list += str.split(genres, ', ')

    genre_list = list(set(genre_list))

    genre_list.sort()

    return genre_list

def get_rating_by_movie_id(id):
    movie = Movie.objects.filter(id=id)[0]
    ratings = Rating.objects.filter(movie=movie)
    rating = 0

    for rate in ratings:
        rating += rate.rating

    rating = rating / len(ratings)

    return rating

def is_movie_rated_by_user(id, user):
    movie = Movie.objects.filter(id=id)[0]
    ratings = Rating.objects.filter(user=user, movie=movie)
    rating = 0
    if len(ratings) > 0:
        rating = ratings[0].rating
    return len(ratings) > 0, rating

def rate_movie(rating, movie_id, user):
    movie = Movie.objects.filter(id=movie_id)[0]
    Rating.objects.create(rating=rating, user=user, movie=movie)

def get_comments_by_movie_id(id):
    movie = Movie.objects.filter(id=id)[0]
    comments = Comment.objects.filter(movie=movie).order_by('-date')
    return comments

def add_or_remove_favorites(movie_id, username):
    movie = Movie.objects.get(id=movie_id)
    user = User.objects.get(username=username)
    check = Favorite.objects.filter(user=user, movie=movie)
    if len(check) > 0:
        for instance in check:
            instance.delete()
    else:
        favorite = Favorite.objects.create(user=user, movie=movie)
        favorite.save()
    
def save_feedback(form_data, user):
    Feedback.objects.get_or_create(user=user, type=form_data.get('category'), message=form_data.get('message'))

def add_comment(form_data, user, movie_id):
    movie = Movie.objects.filter(id=movie_id)[0]
    Comment.objects.get_or_create(user=user, movie=movie, comment=form_data.get('comment'))

def check_user_favorite(movie_id, user):
    movie = Movie.objects.filter(id=movie_id)[0]
    fav = Favorite.objects.filter(user=user, movie=movie)
    return len(fav) > 0