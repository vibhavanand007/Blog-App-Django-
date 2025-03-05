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
    """Handles user profile update with image deletion logic."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            profile = p_form.save(commit=False)

            # ✅ Delete old Cloudinary image if a new one is uploaded (except default)
            if 'image' in request.FILES:
                old_image_id = profile.image.public_id if profile.image else None

                if old_image_id and old_image_id != "qccfuwidka0xmyyer58i":
                    cloudinary.uploader.destroy(old_image_id)

            profile.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)