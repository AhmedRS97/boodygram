''' use this instead of the default hashing method
from passlib.hash import pbkdf2_sha256 '''

from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birthday = models.DateField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('o', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday', 'gender']
    
class Comments(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField()
    date = models.DateTimeField()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='user')
    date = models.DateTimeField()
    description = models.TextField()
    tag_user = models.ForeignKey(User, related_name='tag_user')
    address = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['address'], zoom=7)
    image = models.ImageField(null=True, blank=True)
    comments = models.ForeignKey(Comments)

