from django.contrib import admin
from .models import User, Comments, Post

# Register your models here.
admin.site.register([User, Comments, Post])
