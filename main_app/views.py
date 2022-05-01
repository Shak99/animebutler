from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import *
# Create your views here.
def index(request):
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

def interest_index(request):
# limit interest to show over if it matches user id
    interests = Interest.objects.filter(user=request.user)
    context = {
        'interests': interests
    }
    return render(request, 'interests/index.html', context)

class AnimeCreate(CreateView):
    model = Anime
    fields = '__all__'
    success_url = '/animes/'

class InterestCreate(CreateView):
    model = Interest
    fields = ['genre']

# tie in the user_id request.user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = '/interests/'

class InterestDelete(DeleteView):
    model = Interest
    success_url = '/interests/'

def animes_index(request):
    animes = Anime.objects.all()
    return render(request, 'animes/anime.html', { 'animes': animes })

def animes_detail(request, anime_id):
    anime = Anime.objects.get(id=anime_id)
    # watchlist_form = watchlistForm()
    return render(request, 'animes/detail.html', {
        'anime': anime, 
    })

# def add_watchlist (request, anime_id):
#   form = watchlistForm(request.POST)
#   if form.is_valid():
#     new_watchlist = form.save(commit=False)
#     new_watchlist.anime_id = anime_id
#     new_watchlist.save()
#   return redirect('detail', anime_id=anime_id)

# def assoc_interest(request, anime_id, interests_id):
#   Anime.objects.get(id=anime_id).interests.add(interests_id)
#   return redirect('detail', anime_id=anime_id)

class WatchlistDetail(ListView):
    model = Watchlist


# class WatchlistCreate(CreateView):
#   model = Watchlist
#   fields = '__all__'

class WatchlistUpdate(UpdateView):
    model = Watchlist
    fields = ['anime', 'interest']

class WatchlistDelete(DeleteView):
    model = Watchlist
    success_url = '/watchlist/'