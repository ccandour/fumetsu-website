from datetime import datetime, timezone
from users.models import Profile
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def Users_time_left(user):
    now = datetime.now(timezone.utc)
    q_user = Profile.objects.filter(user=user)
    g = Group.objects.get(name='nap_vip')
    if not q_user.filter(nap_vip__gte = now):
        g.user_set.remove(user)
    else:
        g.user_set.add(user)

    g = Group.objects.get(name='vip')
    if not q_user.filter(time_vip__gte=now):
        g.user_set.remove(user)
    else:
        g.user_set.add(user)


def check_ban(user):
    now = datetime.now(timezone.utc)
    q_user = Profile.objects.filter(user=user)

    q_users = q_user.filter(Q(ban__isnull=True) | Q(ban__gt=now))
    if q_users.count() > 0 and q_user.first().ban != None:
        return True  # ma bana
    else:
        return False


def Nap_time():
        return True

def Is_member(user):
    VALID_GROUP_EXTENSIONS = [
        "vip",
        "Informator",
        "Uploader",
        "content_creator",
    ]

    for e in VALID_GROUP_EXTENSIONS:
        if User.objects.filter(groups__name=e, id=user.id).first():
            return True

    return False

def Get_color(user):
    Users_time_left(user)
    VALID_GROUP_EXTENSIONS = [
        ["God", "#AD0F3F"],
        ["Moderator", "#4B0082"],
        ["content_creator", "#DAF7A6"],
        ["Biuro", "#FF61DB"],
        ["Informator", "#4AC414"],
        ["Uploader", "#E9C12C"],
        ["vip", "#0E2AA9"],
        ["nap_vip", "#1EBAE4"],
    ]

    i=0
    for e in range(len(VALID_GROUP_EXTENSIONS)):
        if User.objects.filter(groups__name=VALID_GROUP_EXTENSIONS[i][0], id=user.id).first():
            return VALID_GROUP_EXTENSIONS[i][1]
        i+=1

    return False