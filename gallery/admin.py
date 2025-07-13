from django.contrib import admin
from .models import Profile, Tag, Image, Like, Dislike
# Register your models here.

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Dislike)
