from django import forms
from .models import Post, User  # importing models
from datetime import datetime
# from dateutil.parser import parse  # string date parser
from django.contrib.auth import authenticate, login, logout
import re


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description','tag_user','address','location','image']
        exclude = ['comments']
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Type anything.'}
            ),
            'tag_user': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder':'Write your address'}
            ),
        }


# User Registration Form
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control','placeholder': 'Confirm Password',
        }
        )
    )

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'birthday', 'password', 'password2',
        ]
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control fname', 'placeholder': 'First Name'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control lname', 'placeholder': 'Last Name'}
            ),
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username'}
            ),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control', 'placeholder': 'Birth Date dd/mm/yyyy',
                'data-select': "datepicker",
            }),
            'gender': forms.Select(
                attrs={'class': 'form-control', 'placeholder': 'Gender'}
            ),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Password'}
            ),
        }

    def clean(self, *args, **kwargs):
        bday = self.cleaned_data['birthday']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        username = self.cleaned_data['username']
        message = "Password must contain at least 2 digits,be at least 2 uppercase and be more than 6 letters."
        if not(1900 <= bday.year <= datetime.now().year):
            raise forms.ValidationError('Birth Date is invalid, Accepted years is 1900 to current day.')
        if len(password) < 6:
            raise forms.ValidationError(message)
        if sum(c.isdigit() for c in password) < 2:
            raise forms.ValidationError(message)
        if sum(c.isupper() for c in password) < 2:
            raise forms.ValidationError(message)
        if password != password2:
            raise forms.ValidationError('Password Must match.')
        if not re.search(r'^[\w.]+$', username):
            raise forms.ValidationError('Usernames can only use letters, numbers, underscores and periods.')
        return super(RegisterForm, self).clean(*args, **kwargs)


# User Login Form
class LoginForm(forms.Form):  # (forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username', }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password', }
        )
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 0:
            raise forms.ValidationError("The user does not exist")
        else:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(LoginForm, self).clean(*args, **kwargs)


class ProfilePhoto(forms.Form):
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={"id": "image-upload", "type": "file", "name": "profile_photo"}
        )
    )


