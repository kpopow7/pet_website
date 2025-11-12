from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from PIL import Image
from django_resized import ResizedImageField

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, db_index=True)

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.username    
class Pet(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    pet_type_choices = [
        ("DG","Dog"),
        ("CT", "Cat"),
        ("OT", "Other")
    ]
    pet_type = models.CharField(max_length=4, choices=pet_type_choices)
    breed = models.CharField(max_length=50, null=True)
    birthdate = models.DateField(null=True)
    on_meds = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default= lambda: CustomUser.objects.get_or_create(username='default')[0], db_index=True)
    pet_image = ResizedImageField(default='pet_pics/pet_placeholder.jpg', upload_to='pet_pics')

    class Meta:
        ordering = ['name']
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'

    def __str__(self):
        return self.name
    

class Stay(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    comments = models.TextField()
    petName = models.ForeignKey(Pet, on_delete=models.CASCADE, db_index=True)
    stay_type_choices = [
        ("S1", "30 Min Drop in"),
        ("S2", "60 Min Drop in"),
        ("S3", "House Sitting"),
    ]
    stay_type = models.CharField(max_length=4, choices=stay_type_choices)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ['title']
        verbose_name = 'Stay'
        verbose_name_plural = 'Stays'

    def __str__(self):
        return self.title

class Photo(models.Model):
    image = ResizedImageField(size=[700, 700], upload_to='gallery/')
    caption = models.CharField(max_length=100)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, db_index=True)
    date_created = models.DateField()

    class Meta:
        ordering = ['caption']
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return self.caption
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_index=True)
    prof_pic = models.ImageField(default='profile_avatars/standard.jpg',upload_to='profile_avatars/')
    street = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=2, null=True)
    zip = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user.username} Profile'
    