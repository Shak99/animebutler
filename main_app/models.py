from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

# Create your models here.
    
GENRES = [
    ('1', 'Action'),
    ('2', 'Adventure'),
    ('4', 'Comedy'),
    ('8', 'Drama'),
    ('10', 'Fantasy'),
    ('14', 'Horror'),
    ('40', 'Psychological'),
    ('22', 'Romance'),
    ('24', 'Sci-Fi'),
    ('25', 'Shoujo'),
    ('27', 'Shounen'),
    ('36', 'Slice of Life'),
]

class Anime(models.Model):
    title = models.CharField(max_length=350)
    producers = ArrayField(models.CharField(max_length=200), size=10, default=list)
    genres = ArrayField(models.CharField(max_length=200), size=10, default=list)
    description = models.CharField(max_length=1000)
    year = models.IntegerField(default=None, null=True)
    episodes = models.IntegerField()
    status = models.CharField(max_length=100, default="Not Available")
    image = models.CharField(max_length=200, default="No url")
    mal_id=models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}'s watchlist "

    def get_absolute_url(self):
        return reverse('watchlist_detail', kwargs={'pk': self.id})
    
    
class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(
        max_length=20,
        choices=GENRES,
        default=GENRES[0][1]
        )
    
    def __str__(self):
        return self.get_genre_display()