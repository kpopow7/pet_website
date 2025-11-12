from django.contrib import admin
from .models import CustomUser, Pet, Stay, Photo, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import Group
#from django.contrib.auth.models import Permission
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "prof_pic",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
class PetAdmin(admin.ModelAdmin):
    list_select_related = ('owner',)
    list_prefetch_related = ('owner',)
    list_display = ('name', 'owner', 'breed', 'birthdate', 'on_meds')
    list_filter = ('owner', 'breed', 'birthdate', 'on_meds')
    search_fields = ('name', 'owner__username', 'breed')
    ordering = ('name',)
    list_per_page = 10
admin.site.register(Pet, PetAdmin)
class StayAdmin(admin.ModelAdmin):
    list_select_related = ('petName',)
    list_prefetch_related = ('petName',)
    list_display = ('petName', 'start_date', 'end_date')
    list_filter = ('petName', 'start_date', 'end_date')
    search_fields = ('petName__name', 'start_date', 'end_date')
    ordering = ('petName',)
    list_per_page = 10
admin.site.register(Stay, StayAdmin)
class PhotoAdmin(admin.ModelAdmin):
    list_select_related = ('pet_id',)
    list_prefetch_related = ('pet_id',)
    list_display = ('pet_id', 'image', 'caption', 'date_created')
    list_filter = ('pet_id', 'date_created')
    search_fields = ('pet_id__name', 'caption')
    ordering = ('pet_id',)
    list_per_page = 10
admin.site.register(Photo, PhotoAdmin)
class ProfileAdmin(admin.ModelAdmin):
    list_select_related = ('user',)
    list_prefetch_related = ('user',)
    list_display = ('user', 'city', 'zip')
    list_filter = ('user', 'city', 'zip')
    search_fields = ('user__username',)
    ordering = ('user',)
    list_per_page = 10
admin.site.register(Profile, ProfileAdmin)
#admin.site.register(Group)
#admin.site.register(Permission)

# Register your models here.
