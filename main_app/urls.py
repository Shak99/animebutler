from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.index_search, name='ind_search'),
    path('animes/genre/<int:genre_id>/', views.search_by_genre, name='genre-search'),
    path('accounts/signup/', views.signup, name='signup'),
    
    # Anime views
    path('animes/', views.animes_index, name='anime'),
    path('animes/<int:anime_id>/', views.animes_detail, name='detail'),
    path('animes/search/', views.search_for_anime, name='search'),
    
    # Watchlist views
    path('watchlist/', views.WatchlistDetail.as_view(), name='watchlist_list'),
    path('watchlist/add_anime/<int:anime_id>', views.add_to_watchlist, name='add_anime'),
    path('watchlist/delete_anime/<int:anime_id>', views.delete_from_watchlist, name='delete_anime'),

    # Interest views
    path('interests/', views.interest_index, name='interest_index'),
    path('interests/create/', views.InterestCreate.as_view(), name='interest_form'),
    path('interests/<int:pk>/delete_interest/', views.InterestDelete.as_view(), name='delete_interest'),
    path('interests/<int:interest_id>/', views.search_by_interest, name='interest-search'),

]