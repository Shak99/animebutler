from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

# Create your models here.
    
GENRES = [
    ('a', 'Action Adventure'),
    ('b', 'Comedy'),
    ('c', 'Drama'),
    ('d', 'Fantasy'),
    ('e', 'Horror'),
    ('f', 'Psychological'),
    ('g', 'Romance'),
    ('h', 'Sci-Fi'),
    ('i', 'Shoujo'),
    ('j', 'Shounen'),
    ('k', 'Slice of Life'),
]

LANG_OPTIONS = (
    ('a', 'Japanese Original'),
    ('b', 'English Dub'),
    ('c', 'Portuguese Dub'),
    ('d', 'Spanish Dub'),
    ('e', 'Original Japanese/English Sub'),
    ('f', 'Original Japanese/Portuguese Sub'),
    ('g', 'Original Japanese/Spanish Sub'),
)

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
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    # anime = models.IntegerField()

    def get_absolute_url(self):
        return reverse('watchlist_detail', kwargs={'pk': self.id})
    
class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(
        max_length=20,
        choices=GENRES,
        default=GENRES[0][0]
        )