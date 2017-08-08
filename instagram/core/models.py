from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birthday = models.DateField()
    gender = models.ChoiceField({"Male": "m", "Female": "f", "Other":"o"})
    email = models.EmailField()
    user = models.CharField()
    password = models.CharField()  ''' widget=forms.PasswordInput)
                                       TODO: how to e
                                   '''
