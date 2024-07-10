from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from PIL import Image, ImageSequence
from django_cleanup import cleanup
from django.core.validators import MaxValueValidator, MinValueValidator


class Relation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child_series_id = models.CharField(max_length=100, null=True, blank=True)
    parent_series_id = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'child: {self.child_series_id} |  ->  | parent: {self.parent_series_id} | -> | type: {self.type}'


class Anime_list(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_anime = models.IntegerField()
    content = models.TextField()
    image = models.ImageField(default='av_default.gif', upload_to='anime_avatar')
    image_bg = models.ImageField(default='anime_bg.jpg', upload_to='anime_avatar')
    napisy = models.FileField(upload_to='archiwum/', blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    web_name = models.CharField(max_length=100, null=True, blank=True)
    # Anilist properties
    name_romaji = models.CharField(max_length=100, null=True, blank=True)
    name_english = models.CharField(max_length=100, null=True, blank=True)
    format = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    episode_count = models.IntegerField(null=True, blank=True)
    anilist_id = models.CharField(max_length=100, null=True, blank=True)
    cover_image = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.web_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        size = [1280, 720]  #wymiary

        img = Image.open(self.image.path)

        if img.height > size[0] or img.width > size[1]:
            img.thumbnail(size)
            img.save(self.image.path)


class Harmonogram(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(Anime_list, on_delete=models.CASCADE)
    content = models.TextField()
    day = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.key_map}'


class Series_comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(Anime_list, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=254)

    def __str__(self):
        return (f'post {self.author}, {self.content} do anime {self.key_map}.')


class Info_bd(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idd = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='akt_default.gif', upload_to='akt_post')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        size = [1280, 720]  #wymiary

        img = Image.open(self.image.path)

        if img.height > size[0] or img.width > size[1]:
            img.thumbnail(size)
            img.save(self.image.path)

    def __str__(self):
        return self.title


class Post_comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_map = models.ForeignKey(Info_bd, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=254)

    def __str__(self):
        return (f'post {self.author}, {self.content} do anime {self.post_map}.')

class Url_redirects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    old_url = models.CharField(max_length=100)
    new_url = models.CharField(max_length=100)
