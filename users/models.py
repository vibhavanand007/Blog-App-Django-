from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Ensure the model instance is saved before processing the image
        super().save(*args, **kwargs)

        # Check if an image exists
        if self.image and hasattr(self.image, 'file'):
            img = Image.open(self.image)

            # Convert to RGB if the image is not already in that mode
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize if necessary
            max_size = (300, 300)
            if img.height > 300 or img.width > 300:
                img.thumbnail(max_size)

            # Save the processed image
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=90)

            # Update the image field
            self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)

            # Save the instance again to persist changes
            super().save(update_fields=['image'])