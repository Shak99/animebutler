from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_for_anime, name='ind_search'),
    path('genre-search/<int:genre_id>/', views.search_by_genre, name='animes-genre'),
    path('accounts/signup/', views.signup, name='signup'),
    
    # Anime views
    path('animes/', views.animes_index, name='anime'),
    path('animes/<int:anime_id>/', views.animes_detail, name='detail'),
    path('animes/create/', views.AnimeCreate.as_view(), name='animes_create'),
    # path('animes/<str:genre_id>/', views.genre_view, name="genre"),
    path('animes/search/', views.search_for_anime, name='search'),
    # path('animes/<int:pk>/delete/', views.AnimeDelete.as_view(), name='animes_delete'),
    
    # Watchlist views
    path('watchlist/', views.WatchlistDetail.as_view(), name='watchlist_list'),
    path('watchlist/add_anime/<int:anime_id>', views.add_to_watchlist, name='add_anime'),
    # path('watchlist/<int:anime_id>/addanime/', views.addToWatchlist.as_view(), name='add_anime'),
    path('watchlist/delete_anime/<int:anime_id>', views.delete_from_watchlist, name='delete_anime'),
    # path('animes/<int:user_id>/delete_watchlist/', views.WatchlistDelete.as_view(), name='delete_watchlist'),

    # Interest views
    path('interests/', views.interest_index, name='interest_index'),
    path('interests/create/', views.InterestCreate.as_view(), name='interest_form'),
    path('animes/<int:pk>/delete_interest/', views.InterestDelete.as_view(), name='delete_interest'),
]