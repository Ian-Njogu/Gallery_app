from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Image, Tag, Like, Dislike, Profile
from django.contrib.auth.models import User
from .forms import ImageForm

# create your views here.

# Homepage – Photo Gallery
def image_list_view(request):
    images = Image.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    return render(request, 'home.html', {'images': images, 'tags': tags})

# View iamage Details
def image_detail_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    likes = image.likes.count()
    dislikes = image.dislikes.count()
    return render(request, 'image_detail.html', {'image': image, 'likes': likes, 'dislikes': dislikes})

# Like a Image
@login_required
def like_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    Like.objects.get_or_create(user=request.user, image=image)
    Dislike.objects.filter(user=request.user, image=image).delete()
    return redirect('image_detail', image_id=image.id)

# Dislike a Image
@login_required
def dislike_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    Dislike.objects.get_or_create(user=request.user, image=image)
    Like.objects.filter(user=request.user, image=image).delete()
    return redirect('image_detail', image_id=image.id)

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
    return render(request, 'register.html', {'form': form})

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
    return render(request, 'login.html', {'form': form})

# Logout User
def logout_view(request):
    logout(request)
    return redirect('login')

# View user profile
@login_required
def profile_view(request):
    return render(request, 'profile.html', {'profile': request.user.profile})

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
    return render(request, 'edit_profile.html')

@login_required
def upload_image_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.save()
            form.save_m2m()  # Save tags
            messages.success(request, "Image uploaded successfully.")
            return redirect('image_list')
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})
