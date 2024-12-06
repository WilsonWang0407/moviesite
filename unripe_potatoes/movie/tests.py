from django.test import TestCase
import json
import random
from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from movie.forms import CommentForm, FeedbackForm, UserRegistrationForm
from movie.helper import (
    get_all_movies,
    get_comments_by_movie_id,
    get_genre_list,
    get_movies_by_genre,
    get_rating_by_movie_id,
    is_movie_rated_by_user,
    rate_movie,
    search_movies_by_name,
    search_suggestions_by_name,
)
from movie.models import Comment, Favorite, Movie, Rating, UnripeUser


class MovieModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(name='The Shawshank Redemption', year=1994)

    def test_movie_creation(self):
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.name, 'The Shawshank Redemption')


class UnripeUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        UnripeUser.objects.create(user=user, picture='path/to/image.jpg')

    def test_unripe_user_creation(self):
        unripe_user = UnripeUser.objects.get(id=1)
        self.assertEqual(unripe_user.user.username, 'testuser')
        self.assertEqual(unripe_user.picture, 'path/to/image.jpg')


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        movie = Movie.objects.create(name='The Shawshank Redemption', year=1994)
        Comment.objects.create(user=user, movie=movie, comment='Great movie!')

    def test_comment_creation(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.comment, 'Great movie!')
        self.assertEqual(comment.user.username, 'testuser')
        self.assertEqual(comment.movie.name, 'The Shawshank Redemption')

class SearchSuggestionsViewTest(TestCase):
    def test_search_suggestions(self):
        response = self.client.get(reverse('movie:search_suggestions') + '?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')


class UserRegistrationFormTest(TestCase):
    def test_form_valid(self):
        form_data = {'username': 'testuser', 'email': 'user@example.com', 'password1': 'testpassword123', 'password2': 'testpassword123'}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {'username': 'testuser', 'email': 'user@example.com', 'password1': 'testpassword123', 'password2': 'wrongpassword'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class FeedbackFormTest(TestCase):
    def test_feedback_form_valid(self):
        form_data = {'category': 'general feedback', 'message': 'This is a test feedback.'}
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid(self):
        form_data = {'message': 'This is a test feedback.'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        form_data = {'comment': 'This is a test comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {'comment': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())


class HelperFunctionsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.movie = Movie.objects.create(name='Gladiator', year=2000, genre='Action')

    @patch('movie.helper.Movie.objects.filter')
    def test_get_movies_by_genre(self, mock_filter):
        mock_filter.return_value = MagicMock()
        movies = get_movies_by_genre('Action', 10)
        self.assertIsNotNone(movies)


    @patch('movie.helper.Movie.objects.filter')
    def test_search_movies_by_name(self, mock_filter):
        mock_filter.return_value.values.return_value = [{'id': 1, 'name': 'Test Search Movie'}]
        movies_json = search_movies_by_name('Search')
        movies = json.loads(movies_json)
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]['name'], 'Test Search Movie')

    @patch('movie.helper.Movie.objects.filter')
    def test_search_suggestions_by_name(self, mock_filter):
        mock_filter.return_value.values_list.return_value = ['Test Movie']
        suggestions = search_suggestions_by_name('Test')
        self.assertIn('Test Movie', suggestions['names'])

    def test_get_genre_list(self):
        Movie.objects.create(name='Test Movie 2', year=2020, genre='Action, Comedy')
        genres = get_genre_list()
        self.assertIn('Action', genres)
        self.assertIn('Comedy', genres)

    def test_get_rating_by_movie_id(self):
        rating = Rating.objects.create(movie=self.movie, rating=4.5)
        retrieved_rating = get_rating_by_movie_id(self.movie.id)
        self.assertEqual(retrieved_rating, 4.5)

    def test_is_movie_rated_by_user(self):
        rating = Rating.objects.create(user=self.user, movie=self.movie, rating=4.5)
        result = is_movie_rated_by_user(self.movie.id, self.user)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 4.5)

    def test_rate_movie(self):
        rate_movie(3.5, self.movie.id, self.user)
        rating = Rating.objects.get(movie=self.movie, user=self.user)
        self.assertEqual(rating.rating, 3.5)

    def test_get_comments_by_movie_id(self):
        comment = Comment.objects.create(user=self.user, movie=self.movie, comment='Test comment')
        comments = get_comments_by_movie_id(self.movie.id)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].comment, 'Test comment')

class PageNotFoundViewTest(TestCase):
    def test_page_not_found(self):
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)


