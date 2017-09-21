from django.shortcuts import render, redirect # it's Crystal clear :3
from .models import Post, User # importing the post model
from .forms import PostForm # importing the PostForm
from django.contrib.auth.decorators import login_required #good decorator

# Create your views here.

#main page view
def MainPage(request):
    return render(request, 'base.html')

# defining the Post Form view
@login_required #the login_required decorator > will check if user is logged in
def PostFormView(request):
    if request.method == "POST":
        # request.FILES is for getting the attached images or files
        form = PostForm(request.POST, request.FILES)
        # checking if the Form data is valid.
        if form.is_valid():
            '''
            (commit=False) means that it will keep the data but will not commit
            it, thus enabling us to modify its values before the final commit.
            '''
            post = form.save(commit=False)
            post.user = User.objects.get(pk=request.user.pk)
            #post.created = timezone.now() # under test
            post.save()
            return redirect('admin/')

    else:
        form = PostForm()
    return render(request, 'post-form.html', {'form':form})
