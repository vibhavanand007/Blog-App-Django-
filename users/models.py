from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from PIL import Image
from io import BytesIO
import cloudinary.uploader


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # ✅ Use Cloudinary public ID for the default image
    image = CloudinaryField('image', default="qccfuwidka0xmyyer58i")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Handles image compression and deletes old images from Cloudinary when updating"""
        
        # Get old profile image before saving the new one
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            old_image_id = old_profile.image.public_id if old_profile.image else None
        except Profile.DoesNotExist:
            old_image_id = None

        # Process and upload new image only if changed
        if self.image and hasattr(self.image, 'file'):
            img = Image.open(self.image)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            max_size = (300, 300)
            img.thumbnail(max_size)

            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=90)

            # Upload optimized image to Cloudinary
            uploaded_image = cloudinary.uploader.upload(img_io.getvalue(), folder="profile_pics/")
            self.image = uploaded_image["public_id"]  # ✅ Store only public ID

        super().save(*args, **kwargs)

        # ✅ Delete old image from Cloudinary if a new one was uploaded (excluding default)
        if old_image_id and old_image_id != "qccfuwidka0xmyyer58i":
            cloudinary.uploader.destroy(old_image_id)