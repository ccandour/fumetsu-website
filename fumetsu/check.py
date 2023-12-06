from django.contrib.auth.models import User

class check_valid():
    max_size = 300
    need_perm = False
    is_vip = False
    is_super = False
    av_size = [128,128]

    VALID_IMAGE_EXTENSIONS = [
        ".jpg",
        ".jpeg",
        ".png",
    ]

    def __init__(self, users):
        if User.objects.filter(is_superuser=False, username = users.username).first():
            self.is_super = True
        else:
            if self.check_user(users):
                self.is_vip = True 
                self.VALID_IMAGE_EXTENSIONS.append(".gif")

            if self.user_is_staff(users):
                self.need_perm = True 
                self.VALID_IMAGE_EXTENSIONS.append(".gif")


    def test(self):
        return self.tes

    def conf(self):
        self.tes = True

    def change_avatar(self, users, file):
        #self.is_vip = True if self.check_user(user)
        #if self.need_perm:
        #    self.conf(users)
        #else:
        #self.check_user(user)
        return True if (self.check_image_type(file) or self.is_super) else False
#or self.is_super  and self.check_file_type(sub)
    def check_up_pic(self, sub, z_file):
        if self.check_file_type(sub):
            return self.check_image_type(z_file) 
        else: 
            return False
#self.user_is_staff(users)
#and self.check_pic(file)

    def check_file_type(self, z_file: str = f'none') -> str:

        VALID_SUB_EXTENSIONS = [
            ".txt",
            ".zip",
            ".7zip",
            ".ass",
        ]

        return True if any([z_file.endswith(e) for e in VALID_SUB_EXTENSIONS]) else False

    def check_image_type(self, z_file):

        return True if any([z_file.name.endswith(e) for e in self.VALID_IMAGE_EXTENSIONS]) else False

    def check_user(self, users):
        VALID_GROUP_EXTENSIONS = [
            "vips",
            "Informators",
            "Uploaders",
            "content_creators",
        ]

        for e in VALID_GROUP_EXTENSIONS:
            if User.objects.filter(groups__name=e, username = self.user.username).first():
                return True

        return False

    def user_is_staff(self, users):

        VALID_GROUP_EXTENSIONS = [
            "Informator",
            "Uploader",
            "content_creator",
        ]

        for e in VALID_GROUP_EXTENSIONS:
            if User.objects.filter(groups__name=e, username = users.username).first():
                return True

        return False