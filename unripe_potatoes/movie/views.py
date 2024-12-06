from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from movie.forms import UserRegistrationForm, UserLoginForm, FeedbackForm, CommentForm
from movie.helper import get_random_movies, get_movies_by_genre, MENU_LINKS, get_all_movies, get_genre_movies, get_movie_by_id, search_suggestions_by_name, get_genre_list, add_or_remove_favorites, save_feedback, add_comment, get_rating_by_movie_id, get_comments_by_movie_id, is_movie_rated_by_user, rate_movie, check_user_favorite, get_fav_movies, get_fav_genre_list

# home page
def index(request):
    carousel_movies = get_random_movies(5)
    popular_movies = get_random_movies(10)
    action_movies = get_movies_by_genre('action', 10)
    comedy_movies = get_movies_by_genre('comedy', 10)

    context = {
        'carousel_movies': carousel_movies,
        'popular_movies': popular_movies,
        'action_movies': action_movies,
        'comedy_movies': comedy_movies,
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }
    return render(request, 'movie/index.html', context)

# all movie list pages
def all_movies(request):
    context = {
        'movies': get_all_movies(request.user),
        'title': 'All Movies',
        'filters': True,
        'genres': get_genre_list(),
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }

    return render(request, 'movie/movie_list.html', context)

def genre_movies(request, genre):
    context = {
        'movies': get_genre_movies(genre, request.user),
        'title': MENU_LINKS[genre],
        'filters': False,
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }

    return render(request, 'movie/movie_list.html', context)

@login_required
def favorite_movies(request):
    context = {
        'movies': get_fav_movies(request.user),
        'title': 'Your Favorites',
        'filters': True,
        'genres': get_fav_genre_list(request.user),
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }


    return render(request, 'movie/movie_list.html', context)

def search_movie(request, q):
    context = {
        'movies': search_suggestions_by_name(q),
        'title': f'Search results for "{q}"',
        'filters': True,
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }

    return render(request, 'movie/movie_list.html', context)

#movie page
def movie(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            add_comment(form.cleaned_data, request.user, id)
            return redirect(f'/movie/{id}')
    else:
        form = CommentForm()

    movie = get_movie_by_id(id)
    rating = get_rating_by_movie_id(id)
    comments = get_comments_by_movie_id(id)
    user_fav = False
    user_rating = [False, 0]
    if (not request.user.username == ''):
        user_rating = is_movie_rated_by_user(id, request.user)
        user_fav = check_user_favorite(id, request.user)

    context = {
        'form': form,
        'movie': movie,
        'title': movie.name,
        'logged_in': not request.user.username == '',
        'favorite': user_fav,
        'rating': rating,
        'user': request.user,
        'user_rating': user_rating[1],
        'already_rated': user_rating[0],
        'menu_links': MENU_LINKS,
        'comments': comments,
        'comments_length': len(comments),
    }

    return render(request, 'movie/movie_page.html', context)

# search suggestions endpoint
def search_suggestions(request):
    q = request.GET.get('q', '')
    return JsonResponse(search_suggestions_by_name(q), safe=False)

# register page
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        if not request.user.username == '': return redirect('/')
        form = UserRegistrationForm()

    context = {
        'form': form,
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }
    return render(request, 'movie/register.html', context)

# login page
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
    else:
        if not request.user.username == '': return redirect('/')
        form = UserLoginForm()

    context = {
        'form': form,
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }
    return render(request, 'movie/login.html', context)

# logout
def logout_user(request):
    logout(request)
    return redirect('/')

# handle favorite endpoint
@login_required
def handle_favorite(request):
    movie_id = request.GET.get('id', '')
    add_or_remove_favorites(movie_id, request.user.username)
    
    return JsonResponse({'message': 'done'})

# feedback page
@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            save_feedback(form.cleaned_data, request.user)
            return redirect('/feedback-success')
    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }

    return render(request, 'movie/feedback.html', context)

@login_required
def feedback_success(request):
    context = {
        'logged_in': not request.user.username == '',
        'user': request.user,
        'menu_links': MENU_LINKS
    }

    return render(request, 'movie/feedback-success.html', context)

@login_required
def add_rating(request):
    movie_id = request.GET.get('movie_id', '')
    rating = request.GET.get('rating', '')
    rate_movie(float(rating), int(movie_id), request.user)
    return redirect(f'/movie/{movie_id}')

def page_404(request, exception):
    return render(request, 'movie/404.html', {}, status=404)