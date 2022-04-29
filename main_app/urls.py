from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('animes/', views.animes_index, name='anime'),
    path('animes/<int:anime_id>/', views.animes_detail, name='detail'),
    path('animes/create/', views.AnimeCreate.as_view(), name='animes_create'),
    # path('animes/<int:pk>/delete/', views.AnimeDelete.as_view(), name='animes_delete'),
    path('watchlist/', views.WatchlistDetail.as_view(), name='watchlist_detail'),
    path('animes/<int:user_id>/update_watchlist/', views.WatchlistUpdate.as_view(), name='update_watchlist'),
    path('animes/<int:user_id>/delete_watchlist/', views.WatchlistDelete.as_view(), name='delete_watchlist'),
    path('interests/create/', views.InterestCreate.as_view(), name='interests_create'),
    path('animes/<int:user_id>/delete_interest/', views.InterestDelete.as_view(), name='delete_interest'),
    path('interests/', views.Interests.as_view(), name='interests'),
]