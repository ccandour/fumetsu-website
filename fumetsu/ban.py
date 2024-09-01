from django.contrib.auth.models import User

def get_color(user):
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

    i = 0
    for e in range(len(VALID_GROUP_EXTENSIONS)):
        if User.objects.filter(groups__name=VALID_GROUP_EXTENSIONS[i][0], id=user.id).first():
            return VALID_GROUP_EXTENSIONS[i][1]
        i += 1

    return False
