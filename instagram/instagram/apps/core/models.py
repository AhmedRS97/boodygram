''' use this instead of the default hashing method
from passlib.hash import pbkdf2_sha256 '''

from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import AbstractBaseUser

#Documentation is a headache for me :3
# Create your models here.
'''
user model that's Inheriting from AbstractBaseUser which is a the django
Built-in User model, it's very handy because it takes care of storing passwords
and Authenticating users.
'''
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=60) #it's      obvious
    last_name = models.CharField(max_length=60)  #    Pretty       :3
    birthday = models.DateField() #obvious too :3
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('o', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64, unique=True)
    '''
    the below is the required Authentication field by AbstractBaseUser, its value
    is the EmailField Cuz I choose it to force the user to authentuicate using it.
    the password is Handled Automatically by the module.
    '''
    USERNAME_FIELD = 'email'
    '''the required fields obviously is the additional fields that will be
       also stored with Email and password'''
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday', 'gender']

class Comment(models.Model):
    user = models.ForeignKey(User) # ForeignKey to the user
    '''parms below is denoting that this field is Optional and django can
       put empty data in it. '''
    comment = models.TextField(null=True, blank=True)
    '''the parm below is needed to force django to populate
       the field with current date on everytime data is saved to this model.'''
    created = models.DateTimeField(auto_now_add=True) # add data.
    updated = models.DateTimeField(auto_now=True) # update data.

#this model is for storing posts as you can see :3
class Post(models.Model):
    user = models.ForeignKey(User, related_name='user') #ForeignKey to user
    '''important note: the parm below is needed to force django to populate
       the field with current date on everytime data is saved to this model.'''
    created = models.DateTimeField(auto_now_add=True) # add data.
    updated = models.DateTimeField(auto_now=True) # update data.
    '''parms below is denoting that this field is Optional and django can
       put empty data in it'''
    description = models.TextField(null=True, blank=True)
    tag_user = models.ForeignKey(User, related_name='tag_user') # taging users
    '''adding address for the location_field, it needs improvements IMO.'''
    address = models.CharField(max_length=255)
    '''PlainLocationField is a field Inherited from location_field Lib.
       though it's javascript have errors !!'''
    location = PlainLocationField(based_fields=['address'], zoom=7)
    image = models.ImageField() #obviously it's an ImageField :3
    comments = models.ForeignKey(Comment) # ForeignKey to the comment
