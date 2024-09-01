from django.db import models
import uuid
from django.utils import timezone
from fumetsu.models import AnimeSeries
from PIL import Image
from django.contrib.auth.models import User


class AnimeEpisode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(AnimeSeries, on_delete=models.CASCADE, null=True)
    ep_nr = models.IntegerField(null=True, blank=True)
    title = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    subtitles = models.FileField(upload_to='subtitles/', blank=True)

    def __str__(self):
        return f'{self.key_map}. Ep nr: {self.ep_nr} tutuł: {self.title}.'


class AnimePost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    odc_nm = models.ForeignKey(AnimeEpisode, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    image = models.ImageField(default='anime_default.jpg', upload_to='anime_post')

    def __str__(self):
        return f'{self.odc_nm}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        size = [300, 300]  #wymiary

        img = Image.open(self.image.path)

        if img.height > size[0] or img.width > size[1]:
            img.thumbnail(size)
            img.save(self.image.path)

        if AnimePost.objects.all().count() > 12:
            AnimePost.objects.all().order_by('odc_nm__date_posted').first().delete()


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(AnimeSeries, on_delete=models.CASCADE, null=True)
    odc_nm = models.ForeignKey(AnimeEpisode, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)  #opis dla adminów na str
    web_site = models.CharField(max_length=100)  #jpdl jaki ze mnie geniusz to jest nazwa playera
    ep_nr = models.IntegerField()
    link = models.TextField()

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anime_anilist_id = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    label_polish = models.CharField(max_length=100)

    def __str__(self):
        return f'tag {self.label} dla anime {self.anime_anilist_id}.'


class EpisodeComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map_ep = models.ForeignKey(AnimeEpisode, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=254)

    def __str__(self):
        return f'post {self.author}, {self.content} do anime {self.key_map_ep}.'
