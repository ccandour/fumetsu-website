from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from PIL import Image, ImageSequence
from django_cleanup import cleanup
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import Profile


class Relation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child_series_id = models.CharField(max_length=100, null=True, blank=True)
    parent_series_id = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'child: {self.child_series_id} |  ->  | parent: {self.parent_series_id} | -> | type: {self.type}'


class Anime_list(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    anilist_id = models.CharField(max_length=100, null=True, blank=True)
    name_romaji = models.CharField(max_length=100, null=True, blank=True)
    name_english = models.CharField(max_length=100, null=True, blank=True)
    web_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()

    format = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    episode_count = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)

    napisy = models.FileField(upload_to='archiwum/', blank=True)

    def __str__(self):
        return f'{self.web_name}'


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

class Staff_credits(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series = models.ForeignKey(Anime_list, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user} as {self.role} in {self.series}'
