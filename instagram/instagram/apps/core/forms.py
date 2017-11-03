# importing ModelForm which it's a django default but not custom form
from django import forms
from .models import Post, User # importing models
from datetime import date
from django.contrib.auth import authenticate, login, logout
import re

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description','tag_user','address','location','image']
        exclude = ['comments']
        widgets = {'description': forms.Textarea(attrs={
            'class': 'form-control', 'placeholder':'Type anything.'}),
        'tag_user': forms.Select(attrs={
            'class': 'form-control'}),
        'address': forms.TextInput(attrs={
            'class': 'form-control', 'placeholder':'Write your address'})
        }

# User Registration Form
class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control','placeholder': 'Confirm Password',}))
    class Meta:
        model = User
        fields = ['email','username','first_name',
                'last_name','birthday','gender',
                'password','password2',
                ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control fname', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control lname', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Username'}),
            # the below line is optional attributes for Date widget
            #attrs={'class': 'form-control','placeholder': 'BirthDate',}),
            'birthday': forms.SelectDateWidget(years=[y for y in range(1950, date.today().year+1)]),

            'gender': forms.Select(attrs={
                'class': 'form-control', 'placeholder': 'Gender'}),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control', 'placeholder': 'Password'}),
        }
    def clean(self, *args, **kwargs):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        username = self.cleaned_data['username']
        message = "Password must contain at least 2 digits,be at least 2 uppercase and be more than 6 letters."
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
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            }),
            'password': forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            }),
        }
