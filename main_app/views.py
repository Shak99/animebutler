from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import *

import requests

# Create your views here.
def index(request):
    # should also show all animes in database
    return render(request, 'index.html')

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

@login_required
def interest_index(request):
# limit interest to show over if it matches user id
    interests = Interest.objects.filter(user=request.user)
    context = {
        'interests': interests
    }
    return render(request, 'interests/index.html', context)

@login_required
def animes_index(request):
    animes = Anime.objects.all()

    return render(request, 'animes/anime.html', { 
        'animes': animes,
        })

def search_for_anime(request):
    print('is search for anime function running?')
    query = request.GET.get('q')
    # print(request.GET.get('q'))
    response = requests.get(f"https://api.jikan.moe/v4/anime?q={query}")
    results = response.json()
    results = results['data']

    return render(request, 'animes/anime.html', {'results' : results})

def animes_detail(request, anime_id):
    anime = Anime.objects.get(id=anime_id)
    # at some point add functionality to add anime to watchlist
    # watchlist_form = watchlistForm()
    return render(request, 'animes/detail.html', {
        'anime': anime, 
    })
    
def genre_view(request, genre_id):
    for genre in GENRES:
        if genre_id == genre[1]:
            anime_genre = Anime.objects.filter (genre = genre[0])
    context = {
        'genres': anime_genre,
        'GENRES': GENRES
    }
    return render(request, 'animes/genre.html', context)
    

def add_to_watchlist(request, anime_id):
    new_anime = Anime.objects.get(id=anime_id)
    Watchlist.objects.create (
                    user=request.user,
                    anime=new_anime
                )
    return redirect('/watchlist/')

def delete_from_watchlist(request, anime_id):
    addedanime = Watchlist.objects.get(anime=anime_id)
    addedanime.delete()
    return redirect('/watchlist/')

# class addToWatchlist(CreateView):
#     model = Watchlist
#     fields = ['anime']

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     success_url = '/watchlist/'

class AnimeCreate(LoginRequiredMixin, CreateView):
    model = Anime
    fields = '__all__'
    success_url = '/animes/'

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

class WatchlistDetail(LoginRequiredMixin, ListView):
    model = Watchlist

class WatchlistUpdate(LoginRequiredMixin, UpdateView):
    model = Watchlist
    fields = ['anime', 'interest']

class WatchlistDelete(LoginRequiredMixin, DeleteView):
    model = Watchlist
    success_url = '/watchlist/'
