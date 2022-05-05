from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, DeleteView
from .models import *
import requests

def index(request):
    return render(request, 'index.html', {'genres': GENRES })

def index_search(request):
    query = request.GET.get('q')
    response = requests.get(f'https://api.jikan.moe/v4/anime?q={query}&order_by"popularity"')
    results = response.json()
    results = results['data']
    context = {
        'results': results,
        'genres': GENRES
    }
    return render(request, 'index.html', context)

def search_by_genre(request, genre_id):
    response = requests.get(f'https://api.jikan.moe/v4/anime?genres={genre_id}&order_by="popularity"')
    genre_results = response.json()
    genre_results = genre_results['data']
    context = {
        'genres': GENRES,
        'results': genre_results
    }
    return render(request, 'index.html', context)

def signup(request):
    error_message = ''
    if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
        # This will add the user to the database
            user = form.save()
        # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# animes/
@login_required
def animes_index(request):
    interests = Interest.objects.filter(user=request.user)
    #print(interests)
    context = {
        'interests': interests,
    }
    return render(request, 'animes/anime.html', context)

def search_for_anime(request):
    query = request.GET.get('q')
    response = requests.get(f'https://api.jikan.moe/v4/anime?q={query}&order_by"popularity"')
    results = response.json()
    results = results['data']
    interests = Interest.objects.filter(user=request.user)
    context = {
        'results': results,
        'interests': interests,
        'genres': GENRES
    }
    return render(request, 'animes/anime.html', context)

@login_required
def search_by_interest(request, interest_id):
    response = requests.get(f'https://api.jikan.moe/v4/anime?genres={interest_id}&order_by="popularity"')
    interest_results = response.json()
    interest_results = interest_results['data']
    interests = Interest.objects.filter(user=request.user)
    context = {
        'results': interest_results,
        'interests': interests,
        'genres': GENRES
    }
    return render(request, 'animes/anime.html', context)

def animes_detail(request, anime_id):
    response = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}")
    anime = response.json()
    anime = anime['data']
    return render(request, 'animes/detail.html', {'anime': anime})

# watchlist/
class WatchlistDetail(LoginRequiredMixin, ListView):
    model = Watchlist
    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)
    

@login_required
def add_to_watchlist(request, anime_id):
    # api request consumption for one anime
    response = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}")
    anime = response.json()
    anime = anime['data']
    # saves api info to a new instance of Anime model
    new_anime = Anime.objects.create(
        title=anime['title'],
        producers =[producer['name'] for producer in anime['producers']],
        genres = [genre['name'] for genre in anime['genres']],
        description = anime['synopsis'][:498],
        year = anime['year'],
        episodes = anime['episodes'],
        status = anime['status'],
        image = anime['images']['jpg']['image_url'],
        mal_id = anime['mal_id']
        # accept mal_id as a separate id for anime to reference api
    )
    # saves anime and user to watchlist
    Watchlist.objects.create (
                    user=request.user,
                    anime=new_anime
                )
    return redirect('/watchlist/')

@login_required
def delete_from_watchlist(request, anime_id):
    addedanime = Watchlist.objects.get(anime=anime_id)
    addedanime.delete()
    return redirect('/watchlist/')

# interests/
class InterestCreate(LoginRequiredMixin, CreateView):
    model = Interest
    fields = ['genre']

    # tie in the user_id request.user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = '/interests/'

class InterestDelete(LoginRequiredMixin, DeleteView):
    model = Interest
    success_url = '/interests/'

@login_required
def interest_index(request):
    # limit interest to show only if it matches user id
    interests = Interest.objects.filter(user=request.user)
    context = {
        'interests': interests
    }
    return render(request, 'interests/index.html', context)