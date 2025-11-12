from django import forms
from .models import Photo, CustomUser, Profile, Pet
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ImageForm(forms.ModelForm):
    class Meta: 
        model = Photo
        fields = ['image', 'caption', 'pet_id', 'date_created']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['street', 'city', 'state', 'zip', 'prof_pic']

class PetPicForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_image']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'birthdate', 'on_meds', 'pet_image']

