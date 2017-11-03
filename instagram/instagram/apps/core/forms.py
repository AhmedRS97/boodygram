# importing ModelForm which it's a django default but not custom form
from django import forms
from .models import Post, User # importing models
from datetime import date

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
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name','birthday','gender','password']
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
