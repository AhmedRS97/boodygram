from django.shortcuts import render
from models.models import User, Post, Comments
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# Create your views here.

def create_user(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create(
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            birthday = birthday,
            email = email,
            user = username,
            password = password
        )

    return HttpResponse('User has been created')
