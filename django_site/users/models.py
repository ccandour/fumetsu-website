import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

from core.storage import OverwriteStorage
from utils.utils import generate_upload_path


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ResizedImageField(crop=['middle', 'center'], size=[500,500], default='default.png', upload_to=generate_upload_path, storage=OverwriteStorage())
    time_joined = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=1024, default='Nic o sobie nie powiem.')
    color = models.CharField(max_length=7, default='#ffffff')

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return self.user.username

    def check_staff(self):
        from core.models import StaffCredit
        if self.user.is_superuser or self.id in StaffCredit.objects.values_list('user_id', flat=True):
            return True

        return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
