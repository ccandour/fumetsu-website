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


class AnimeEpisode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(AnimeSeries, on_delete=models.CASCADE, null=True)
    ep_nr = models.IntegerField(null=True, blank=True)
    title = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    subtitles = models.FileField(upload_to='subtitles/', blank=True)

    class Meta:
        db_table = 'fumetsu_anime_episode'

    def __str__(self):
        return f'{self.key_map}. Ep nr: {self.ep_nr} tutuł: {self.title}.'


class AnimePost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    odc_nm = models.ForeignKey(AnimeEpisode, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    image = models.ImageField(default='anime_default.jpg', upload_to='anime_post')

    class Meta:
        db_table = 'fumetsu_anime_post'

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
    title = models.CharField(max_length=100)
    web_site = models.CharField(max_length=100)
    ep_nr = models.IntegerField()
    link = models.TextField()

    class Meta:
        db_table = 'fumetsu_player'

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anime_anilist_id = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    label_polish = models.CharField(max_length=100)

    class Meta:
        db_table = 'fumetsu_tag'

    def __str__(self):
        return f'tag {self.label} dla anime {self.anime_anilist_id}.'


class EpisodeComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map_ep = models.ForeignKey(AnimeEpisode, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=254)

    class Meta:
        db_table = 'fumetsu_episode_comment'

    def __str__(self):
        return f'post {self.author}, {self.content} do anime {self.key_map_ep}.'


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
