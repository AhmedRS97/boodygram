from django.contrib import admin
from .models import User, Comment, Post

# Register your models here.
admin.site.register([User, Comment, Post])
