from django.urls import path
from main_site import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import new_pet, PetListView, ImageListView, PetUpdateView, PetDetailView

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='main_site/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='main_site/logout.html'), name="logout"),
    path('register/', views.register_view, name="register_view"),
    path('about/', views.about, name="about"),
    path('photo_gallery/', ImageListView.as_view(), name="photo_gallery"),
    path('my_profile/', views.profile_view, name="profile_view"),
    path('my_profile/update/', views.my_profile, name="my_profile"),
    path('my_pets/', PetListView.as_view(), name="my_pets" ),
    path('my_pets/<int:pk>/', PetUpdateView.as_view(), name="pet_update"),
    path('my_bookings/', views.my_bookings, name="my_bookings"),
    path('my_profile/new_pet/', new_pet.as_view(template_name='main_site/new_pet.html'), name="new_pet"),
    path('upload/', views.image_upload_view, name="image_upload"),
]

     #Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)