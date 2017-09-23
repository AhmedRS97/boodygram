# importing ModelForm which it's a django default but not custom form
from django.forms import ModelForm
from .models import Post # importing the post models

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description','tag_user','address','location','image']
        exclude = ['comments']
