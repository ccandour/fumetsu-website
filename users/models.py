from django.db import models
from django.contrib.auth.models import User
import uuid
from PIL import Image
from django.utils import timezone

from utils.utils import generate_upload_path


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=generate_upload_path)
    time_joined = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=1024, default='Nic o sobie nie powiem.')
    color = models.CharField(max_length=7, default='#ffffff')

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return self.user.username

    def check_staff(self):
        from fumetsu.models import StaffCredit
        if self.user.is_superuser or self.id in StaffCredit.objects.values_list('user_id', flat=True):
            return True

        return False

    def save(self, *args, **kwargs):

        # Check if the profile is being created
        if self.pk is None or Profile.objects.filter(pk=self.pk).exists() is False:
            super().save(*args, **kwargs)
            return

        # Check if the image has changed
        if self.pk:
            old_image = Profile.objects.get(pk=self.pk).image
        else:
            old_image = None

        super().save(*args, **kwargs)

        size = (256, 256)
        if User.objects.filter(is_superuser=True, username=self.user.username).first():
            size = (1024, 1024)

        img = Image.open(self.image.path)

        if (img.format in ('GIF') and self.check_staff()) or (img.format in ('PNG', 'JPEG')):
            if img.height > size[0] or img.width > size[1]:
                img.thumbnail(size)
                img.save(self.image.path)
        else:
            img.thumbnail(size)
            img.save(self.image.path)

        # Restore the old image if it hasn't changed
        if old_image and self.image == 'default.jpg':
            self.image = old_image
            super().save(update_fields=['image'])
