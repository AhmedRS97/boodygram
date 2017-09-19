from django.shortcuts import render, redirect # it's Crystal clear :3
from .models import Post, User # importing the post model
from .forms import PostForm # importing the PostForm
from django.http import HttpResponse

#project_phase = get_model('core', 'project_phase') # i'm kinda lazy :D

# Create your views here.
#main page view
def MainPage(request):
    '''it was having error : template doesn't exist :( '''
    return render(request, 'base.html')

# defining the Post view :3
def PostFormView(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user #User.object.get(pk=) #workaround ?
            #post.created = timezone.now() # under test
            post.save()
            return redirect('admin/') #, pk=post.pk)

    else:
        form = PostForm()
    return render(request, 'post-form.html', {'form':form})
