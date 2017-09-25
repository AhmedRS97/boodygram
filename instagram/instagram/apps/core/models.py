''' use this instead of the default hashing method
from passlib.hash import pbkdf2_sha256 '''

from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import AbstractUser

#Documentation is a headache for me :3
# Create your models here.
'''
user model that's Inheriting from AbstractUser which is a django Built-in
User model, it's very handy because it takes care of storing/hashing passwords
and Authenticating users.
'''
class User(AbstractUser):
    first_name = models.CharField(max_length=60) #it's      obvious
    last_name = models.CharField(max_length=60)  #    Pretty       :3
    birthday = models.DateField() #obvious too :3
    biography = models.TextField(null=True, blank=True) # data isn't required
    avatar = models.ImageField(null=True, blank=True) # data isn't required
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('o', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64, unique=True)
    '''
    the below is the required Authentication field by AbstractUser, its value is
    the EmailField Cuz I choose it to force the user to authentuicate using it.
    the password is Handled Automatically by the module.
    '''
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    '''the required fields obviously is the additional fields that will be
       also stored with Email and password'''

    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday', 'gender']
    privateAccount = models.BooleanField(default=False)
    '''
    this method is responsible for making the account private.
    '''
    def setAccountToBePrivate(self):
        self.privateAccount = True
    '''
    this method is responsible for making the account public.
    '''
    def setAccoutToBePublic(self):
        self.privateAccount = False

class Comment(models.Model):
    user = models.ForeignKey(User) # ForeignKey to the user
    comment = models.TextField() # comment data is required
    '''the params below is needed to force django to populate
       the field with current date on everytime data is saved to this model.'''
    created = models.DateTimeField(auto_now_add=True) # add current date.
    updated = models.DateTimeField(auto_now=True) # update date.

#this model is for storing posts as you can see :3
class Post(models.Model):
    user = models.ForeignKey(User, related_name='user') #ForeignKey to user
    '''important note: the params below is needed to force django to populate
       the field with current date on everytime data is saved to this model.'''
    created = models.DateTimeField(auto_now_add=True) # add current date.
    updated = models.DateTimeField(auto_now=True) # update date.
    '''params below is denoting that this field is Optional and django can
       put empty data in it'''
    description = models.TextField(null=True, blank=True) # data isn't required
    '''tagging users, I think there's a logical error here.
     it will be changed soon to tag people on photos instead.
     also it isn't required.
     '''
    tag_user = models.ForeignKey(User, related_name='tag_user',null=True, blank=True)
    '''adding address for the location_field, it needs improvements IMO.'''
    address = models.CharField(max_length=255, null=True, blank=True)
    '''PlainLocationField is a field Inherited from location_field Lib.
       though its javascript is having errors! no data is required'''
    location = PlainLocationField(based_fields=['address'], zoom=7,null=True, blank=True)
    image = models.ImageField() #obviously it's an ImageField :3
    # ForeignKey to the comment, though it's not required
    comments = models.ForeignKey(Comment,null=True, blank=True)

'''many to many relationship back into (User model) follow model, I don't think
that it will work properly. I think it must use IntegerField instead of ForeignKey'''
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="Follower")
    followDate = models.DateField(auto_now=True)
    followed = models.ForeignKey(User, related_name="Followed")
