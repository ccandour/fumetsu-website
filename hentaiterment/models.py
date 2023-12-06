from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from PIL import Image, ImageSequence
from django_cleanup import cleanup

class KH_Key_map(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	id_anime = models.IntegerField()
	title = models.CharField(max_length=100)
	web_name = models.CharField(max_length=100)
	
	def __str__(self):
		return  f'{self.title}'

class KH_Anime_list(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	key_map = models.ForeignKey(KH_Key_map, on_delete=models.CASCADE)
	content = models.TextField()
	image = models.ImageField(default='av_default.gif', upload_to='kh_anime_avatar')
	image_bg = models.ImageField(default='anime_bg.jpg', upload_to='kh_anime_avatar')

	def __str__(self):
		return f'{self.key_map}'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		size = [1280,720] #wymiary 

		img = Image.open(self.image.path)

		if img.height > size[0] or img.width > size[1]:
			img.thumbnail(size)
			img.save(self.image.path)

class KH_Odc_name(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key_map = models.ForeignKey(KH_Key_map, on_delete=models.CASCADE, null=True)
    ep_nr = models.IntegerField(null=True, blank=True)
    ep_title = models.FloatField()
    title = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    napisy = models.FileField(upload_to='kh_napisy/', blank=True)

    def __str__(self):
        return ( f'{self.key_map}. Ep nr: {self.ep_nr} tutuł: {self.title}.')

class KH_Anime_url(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    odc_nm = models.ForeignKey(KH_Odc_name, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)#opis dla adminów na str
    web_site = models.CharField(max_length=100)#jpdl jaki ze mnie geniusz to jest nazwa playera
    ep_nr = models.IntegerField()
    link = models.TextField()
    
    def __str__(self):
        return self.title


class KH_Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    odc_nm = models.ForeignKey(KH_Odc_name, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    image = models.ImageField(default='anime_default.jpg', upload_to='kh_anime_post')

    def __str__(self):
        return f'{self.odc_nm}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        size = [300,300] #wymiary 

        img = Image.open(self.image.path)

        if img.height > size[0] or img.width > size[1]:
            img.thumbnail(size)
            img.save(self.image.path)
            
        if KH_Post.objects.all().count() >= 9:
            KH_Post.objects.all().order_by('odc_nm__date_posted').first().delete()