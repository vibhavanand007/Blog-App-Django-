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

            # Get old image's public_id if it exists and is not the default
            old_image_id = None
            if profile.image and isinstance(profile.image, str) and "res.cloudinary.com" in profile.image:
                old_image_id = profile.image.split("/")[-1].split(".")[0]

            # Upload new image if provided and non-empty
            new_image = request.FILES.get('image')
            if new_image and hasattr(new_image, 'size') and new_image.size > 0:
                try:
                    # Rewind the file pointer to ensure the file is not empty
                    new_image.seek(0)
                    uploaded_image = cloudinary.uploader.upload(
                        new_image,
                        folder="profile_pics/"
                    )
                    # Store only the public_id
                    profile.image = uploaded_image["public_id"]
                except Exception as e:
                    print("Error uploading image:", e)
                    messages.error(request, "There was a problem uploading your image. Please try again.")
                    return redirect('profile')

            profile.save()
            messages.success(request, 'Your profile has been updated!')

            # Delete old image from Cloudinary if a new one was uploaded (and it's not the default)
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