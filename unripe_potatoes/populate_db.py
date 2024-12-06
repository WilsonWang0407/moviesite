import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unripe_potatoes.settings')

import csv
import requests
import django
import json
import time

django.setup()

from movie.models import Movie, Rating

def populate():

    tmdb_details_url = 'https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id&api_key=44c1ffbaa897fc99dc16bde3ce0fc7d3'
    tmdb_providers_url = 'https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers?api_key=44c1ffbaa897fc99dc16bde3ce0fc7d3'

    headers = {
        "accept": "application/json"
    }

    thumbnail_url = 'https://image.tmdb.org/t/p/w500{img_name}'
    poster_url = 'https://image.tmdb.org/t/p/w1280{img_name}'

    with open('imdb_top250_movies.csv', 'r') as f:
        movies = csv.DictReader(f)
        for _, movie in enumerate(movies):
            response = requests.get(tmdb_details_url.format(imdb_id=movie['imdbID']), headers=headers)
            tmdb_details = json.loads(response.text)['movie_results'][0]
            
            tmdb_id = tmdb_details['id']
            
            response = requests.get(tmdb_providers_url.format(tmdb_id=tmdb_id), headers=headers)
            tmdb_providers = json.loads(response.text)['results']

            name = movie['Title']
            poster = poster_url.format(img_name=tmdb_details['backdrop_path'])
            thumbnail = thumbnail_url.format(img_name=tmdb_details['poster_path'])
            description = movie['Plot']
            link = tmdb_providers['GB']['link'] if 'GB' in tmdb_providers.keys() else ''
            genre = movie['Genre']
            year = int(movie['Year'])
            runtime = movie['Runtime']
            rating = float(movie['imdbRating'])
            
            add_movie(poster, thumbnail, name, description, link, genre, year, runtime, rating)
            
            print(f'- {name} from the year {year} added')
            
            time.sleep(1 / 51) # To limit execution in tmdb free api rules

def add_movie(poster, thumbnail, name, description, link, genre, year, runtime, rating):
    movie = Movie.objects.get_or_create(name=name, year=year)[0]
    movie.poster = poster
    movie.thumbnail = thumbnail
    movie.description = description
    movie.link = link
    movie.genre = genre
    movie.runtime = runtime
    movie.save()
    movie_rating = Rating.objects.get_or_create(movie=movie, rating=rating)[0]
    movie_rating.save()
    return movie

if __name__ == '__main__':
    print('Starting DB population')
    populate()