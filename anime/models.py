from django.db import models
import uuid
from django.utils import timezone
from fumetsu.models import Anime_list
from django_cleanup import cleanup
from PIL import Image
from django.contrib.auth.models import User

class Odc_name(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(Anime_list, on_delete=models.CASCADE, null=True)
    ep_nr = models.IntegerField(null=True, blank=True)
    ep_title = models.FloatField()
    title = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    napisy = models.FileField(upload_to='napisy/', blank=True)

    def __str__(self):
        return ( f'{self.key_map}. Ep nr: {self.ep_nr} tutuł: {self.title}.')


        

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    odc_nm = models.ForeignKey(Odc_name, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    image = models.ImageField(default='anime_default.jpg', upload_to='anime_post')

    def __str__(self):
        return f'{self.odc_nm}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        size = [300,300] #wymiary 

        img = Image.open(self.image.path)

        if img.height > size[0] or img.width > size[1]:
            img.thumbnail(size)
            img.save(self.image.path)
            
        if Post.objects.all().count() >= 9:
            Post.objects.all().order_by('odc_nm__date_posted').first().delete()


class Anime_url(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(Anime_list, on_delete=models.CASCADE, null=True)
    odc_nm = models.ForeignKey(Odc_name, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)#opis dla adminów na str
    web_site = models.CharField(max_length=100)#jpdl jaki ze mnie geniusz to jest nazwa playera
    ep_nr = models.IntegerField()
    link = models.TextField()
    
    def __str__(self):
        return self.title


class Tags_map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()

    def __str__(self):
        return self.title
        
class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags_map = models.ForeignKey(Tags_map, on_delete=models.CASCADE, null=True)
    key_map = models.ForeignKey(Anime_list, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return ( f'anime: {self.key_map} o tagu: {self.tags_map}.')


class Episode_comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map_ep = models.ForeignKey(Odc_name, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=254)

    def __str__(self):
        return (f'post {self.author}, {self.content} do anime {self.key_map_ep}.')


class Player_valid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map_ep = models.ForeignKey(Odc_name, on_delete=models.CASCADE, null=True)
    ilosc = models.IntegerField(default=1)

    def __str__(self):
        return (f'anime {self.key_map_ep.key_map}, odc: {self.key_map_ep.ep_title}, i ilość: {self.ilosc}.')


