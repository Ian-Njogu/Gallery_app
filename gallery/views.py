from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Image, Tag, Like, Dislike, Profile
from django.contrib.auth.models import User

# create your views here.

# Homepage – Photo Gallery
def photo_list_view(request):
    photos = Image.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    return render(request, 'gallery/home.html', {'photos': photos, 'tags': tags})

# View Photo Details
def photo_detail(request, photo_id):
    photo = get_object_or_404(Image, id=photo_id)
    likes = photo.likes.count()
    dislikes = photo.dislikes.count()
    return render(request, 'gallery/photo_detail.html', {'photo': photo, 'likes': likes, 'dislikes': dislikes})

# Like a Photo
@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Image, id=photo_id)
    Like.objects.get_or_create(user=request.user, image=photo)
    Dislike.objects.filter(user=request.user, image=photo).delete()
    return redirect('photo_detail', photo_id=photo.id)

# Dislike a Photo
@login_required
def dislike_photo(request, photo_id):
    photo = get_object_or_404(Image, id=photo_id)
    Dislike.objects.get_or_create(user=request.user, image=photo)
    Like.objects.filter(user=request.user, image=photo).delete()
    return redirect('photo_detail', photo_id=photo.id)

# Register New User
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('gallery')
    else:
        form = UserCreationForm()
    return render(request, 'gallery/register.html', {'form': form})

# Login User
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gallery')
    else:
        form = AuthenticationForm()
    return render(request, 'gallery/login.html', {'form': form})

# Logout User
def logout_view(request):
    logout(request)
    return redirect('login')

# View user profile
@login_required
def profile_view(request):
    return render(request, 'gallery/profile.html', {'profile': request.user.profile})

# Update profile
@login_required
def update_profile(request):
    if request.method == 'POST':
        bio = request.POST.get('bio')
        pic = request.FILES.get('profile_picture')
        profile = request.user.profile
        profile.bio = bio
        if pic:
            profile.profile_picture = pic
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'gallery/edit_profile.html')
