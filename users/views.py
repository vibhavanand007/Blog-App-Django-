from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import cloudinary.uploader
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Handles user profile update with Cloudinary image deletion logic."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save(commit=False)

            # Check if a new image file is provided and if it is non-empty
            new_image = request.FILES.get('image')
            if new_image and hasattr(new_image, 'size') and new_image.size and new_image.size > 0:
                try:
                    # Upload the new image to Cloudinary
                    uploaded_image = cloudinary.uploader.upload(
                        new_image,
                        folder="profile_pics/"
                    )
                    # Store only the public_id in the profile
                    profile.image = uploaded_image["public_id"]
                except Exception as e:
                    print("Error uploading image:", e)
                    messages.error(request, "There was a problem uploading your image. Please try again.")
                    return redirect('profile')

            profile.save()
            messages.success(request, 'Your profile has been updated!')

            # Attempt to delete the old image (if applicable)
            # Extract the old image public_id if the current image is a Cloudinary image URL
            # (Assumes default public_id is "qccfuwidka0xmyyer58i")
            old_image_id = None
            if profile.image and isinstance(profile.image, str) and "res.cloudinary.com" in profile.image:
                old_image_id = profile.image.split("/")[-1].split(".")[0]
            
            # Delete the old image if it exists and isn't the default
            if old_image_id and old_image_id != "qccfuwidka0xmyyer58i":
                try:
                    cloudinary.uploader.destroy(old_image_id)
                except Exception as e:
                    print(f"Cloudinary deletion error: {e}")

            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)