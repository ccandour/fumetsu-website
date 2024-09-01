from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from PIL import Image


from users.models import Profile


class Relation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child_series_id = models.CharField(max_length=100, null=True, blank=True)
    parent_series_id = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'fumetsu_relation'

    def __str__(self):
        return f'child: {self.child_series_id} |  ->  | parent: {self.parent_series_id} | -> | type: {self.type}'


class AnimeSeries(models.Model):
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

    class Meta:
        db_table = 'fumetsu_anime_series'

    def __str__(self):
        return f'{self.web_name}'


class SeriesComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(AnimeSeries, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=254)

    class Meta:
        db_table = 'fumetsu_series_comment'

    def __str__(self):
        return (f'post {self.author}, {self.content} do anime {self.key_map}.')


class Announcement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idd = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='akt_post')

    class Meta:
        db_table = 'fumetsu_announcement'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        size = [1280, 720]

        img = Image.open(self.image.path)

        if img.height > size[0] or img.width > size[1]:
            img.thumbnail(size)
            img.save(self.image.path)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_map = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=254)

    class Meta:
        db_table = 'fumetsu_post_comment'

    def __str__(self):
        return (f'post {self.author}, {self.content} do anime {self.post_map}.')


class UrlRedirect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    old_url = models.CharField(max_length=100)
    new_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'fumetsu_url_redirect'


class StaffCredit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series = models.ForeignKey(AnimeSeries, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=100)

    class Meta:
        db_table = 'fumetsu_staff_credit'

    def __str__(self):
        return f'{self.user} as {self.role} in {self.series}'
