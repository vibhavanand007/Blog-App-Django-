from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Handles image processing and deleting old images"""
        # Get previous image path before saving new one
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            old_image_path = old_profile.image.path if old_profile.image and old_profile.image.name != 'default.jpg' else None
        except Profile.DoesNotExist:
            old_image_path = None

        super().save(*args, **kwargs)

        # Open and process the new image
        if self.image and hasattr(self.image, 'file'):
            img = Image.open(self.image)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            max_size = (300, 300)
            img.thumbnail(max_size)

            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=90)

            self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)
            super().save(update_fields=['image'])

        # Delete old image (if a new one was uploaded)
        if old_image_path and os.path.exists(old_image_path):
            os.remove(old_image_path)