from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.signals import user_logged_in
from datetime import datetime, timezone
from django.contrib import messages
from django.db.models import Q


def check_ban(sender, user, request, *args, **kwargs):
    now = datetime.now(timezone.utc)
    q_user = Profile.objects.filter(user=user)
    q_users = q_user.filter(Q(ban__isnull=True) | Q(ban__gt=now))
    if q_users.count() > 0 and q_user.first().ban != None:
        messages.success(request, f"jesteś zbanowany do {q_user.first().ban}")
        #logout(request)


user_logged_in.connect(check_ban)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
