from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageForm, CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm, PetPicForm, PetForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views import View
from django.contrib import messages
from .models import CustomUser, Pet, Profile, Photo
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def profile_view(request):
    return render(request, 'view_profile.html')

#@login_required(login_url='/login')
#def photo_gallery(request):

    #return render(request, 'main_site/photo_gallery.html')

#updating this code per cursor recommendation
#class ImageListView(LoginRequiredMixin, ListView):
#    login_url='/login/'
#    model = Photo
#    template_name = 'main_site/photo_gallery.html'
#    context_object_name = 'images'

class ImageListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'main_site/photo_gallery.html'
    context_object_name = 'images'
    
    def get_queryset(self):
        return Photo.objects.select_related('pet_id').all()


@login_required(login_url='/login/')
#@user_passes_test(lambda u: u.is_authenticated)
def my_profile(request):
    if request.method == 'POST':
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/my_profile/')
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
       
    return render(request, 'main_site/my_profile.html', context)

@login_required(login_url='/login/')
#@user_passes_test(lambda u: u.is_authenticated)
def my_pets(request):
    return render(request, 'main_site/my_pets.html')

@login_required(login_url='/login/')
def my_bookings(request):
    return render(request, 'main_site/my_bookings.html')

@login_required(login_url='/login/')
#@user_passes_test(lambda u: u.is_authenticated)
def image_upload_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        messages.success(request, 'Image uploaded successfully')
        return redirect('/photo_gallery/')
    else:
        form = ImageForm()
        return render(request, 'main_site/photo_gallery.html', {'form': form})


#@user_passes_test(lambda u: not u.is_authenticated)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)  #fixed this line and below per cursor recommendation
        if not user: 
            messages.error(request, "Invalid username or password")
            return redirect('/login/')
        login(request, user)
        return redirect('/')
    return render(request, 'main_site/login.html')


#@user_passes_test(lambda u: not u.is_authenticated)
def register_view(request):    
    if request.method == 'POST':         
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created! You may now login')
            return redirect('/login/')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = CustomUserCreationForm()    
    return render(request, 'main_site/register.html', {'form': form})

#@user_passes_test(lambda u: u.is_authenticated)
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('/login/')
    return render(request, 'main_site/logout.html')
    
#updating this code per cursor recommendation
#class PetListView(ListView):
#    model = Pet
#    template_name = 'main_site/my_pets.html'
#    context_object_name = 'pets'
#    def get_queryset(self):
#        return Pet.objects.filter(owner=self.request.user)


class PetListView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = 'main_site/my_pets.html'
    context_object_name = 'pets'
    
    def get_queryset(self):
        return Pet.objects.select_related('owner').filter(owner=self.request.user)
    
class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'main_site/new_pet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class new_pet(LoginRequiredMixin, CreateView):
    model = Pet
    template_name = 'main_site/new_pet.html'
    fields = '__all__'
    success_url = '/my_profile/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'The pet was successfully created')
        return super(new_pet, self).form_valid(form)
     
class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    template_name = 'main_site/new_pet.html'
    fields = ['name', 'pet_type', 'breed', 'birthdate', 'on_meds', 'pet_image']
    pk_url_kwarg = 'pk'
    success_url = '/my_pets/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The pet was successfully updated')
        return super(PetUpdateView, self).form_valid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'main_site/my_profile.html'
    fields = '__all__'
    success_url = '/my_profile/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The profile was successfully updated')
        return super(ProfileUpdateView, self).form_valid(form)


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = 'main_site/my_pets.html'
    success_url = '/my_pets/'

    def form_valid(self, form):
        messages.success(self.request, 'The pet was successfully deleted')
        return super(PetDeleteView, self).form_valid(form)
    
