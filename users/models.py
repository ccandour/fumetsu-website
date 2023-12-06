from django.db import models
from django.contrib.auth.models import User
import uuid
from PIL import Image
from django_cleanup import cleanup
from django.utils import timezone



class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    time_vip  = models.DateTimeField(default=timezone.now)
    nap_vip = models.DateTimeField(default=timezone.now)
    ban = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=1024, default='nic o sobie nie powiem.')
    web_name = models.CharField(max_length=150, null=True, blank=True)
    nick = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


    def check_user(self):
        VALID_GROUP_EXTENSIONS = [
            "vip",
            "Informator",
            "Uploader",
            "content_creator",
        ]

        for e in VALID_GROUP_EXTENSIONS:
            if User.objects.filter(groups__name=e, username = self.user.username).first():
                return True

        return False


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.nick:
            self.nick = self.user.username

        alphanumeric = [character for character in self.nick if character.isalnum()]
        self.web_name = "".join(alphanumeric)

        size = [256,256] #wymiary 128 x 128 
        if User.objects.filter(is_superuser=True, username = self.user.username).first():
            size = [1024,1024]

        img = Image.open(self.image.path)

        if ((img.format in ('GIF') and self.check_user()) or (img.format in ('PNG','JPEG'))):
            if img.height > size[0] or img.width > size[1]:
                img.thumbnail(size)
                img.save(self.image.path)
        else:
            
            img.thumbnail(size)
            img.save(self.image.path)