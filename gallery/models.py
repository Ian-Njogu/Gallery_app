from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField   


# Create your models here.


#Profile model to store user profile information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

# tag model to categorize images
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


# Image model to store images uploaded by users
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_file = CloudinaryField('image', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ['-created_at']

# helper function to get likes/dislikes count
def like_count(self):
    return self.likes.count()

def dislike_count(self):
    return self.dislikes.count()

# Like model to store likes on images
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.image.title}"

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        
# Dislike model to store dislikes on images
class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='dislikes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} dislikes {self.image.title}"

    class Meta:
        verbose_name = 'Dislike'
        verbose_name_plural = 'Dislikes'