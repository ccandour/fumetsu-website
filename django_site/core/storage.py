import os
import shutil

from django.core.files.storage import FileSystemStorage

from core.settings import MEDIA_ROOT


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        cache_path = os.path.join(MEDIA_ROOT, 'CACHE', 'images', os.path.splitext(name)[0])
        if os.path.isdir(cache_path):
            shutil.rmtree(cache_path)
        return name