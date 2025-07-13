from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list_view, name='image_list'),
    path('image/<int:image_id>/', views.image_detail_view, name='image_detail'),
    path('image/<int:image_id>/like/', views.like_image, name='like_image'),
    path('image/<int:image_id>/dislike/', views.dislike_image, name='dislike_image'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.update_profile, name='edit_profile'),
    path('upload/', views.upload_image_view, name='upload_image'),
]