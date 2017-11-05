from django.shortcuts import render, redirect
from .models import * # importing the models
from .forms import * # importing the forms
from django.contrib.auth.decorators import login_required #good decorator
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator # the good ol' paginator :D

# Create your views here.

#Register view
def Register(request):
    '''
    a Register view that validate a form's data and save it to database, then
    it authenticate and login the user and redirect to the user profile page.
    if the form's data is invalid it will render the same page and form's data
    but with warnings.
    '''
    form = RegisterForm(request.POST)
    if form.is_valid():
        #(commit=False) means that it will keep the data but will not commit it.
        # thus enabling us to modify its values before the final commit.
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/'+username)
    else:
        return render(request, 'base.html', {
            'signupform':form,
            'loginform':LoginForm()})

def Login(request):
    '''
    a Login view that validates the form's data and authenticate and login the
    user and redirect the user to the profile page. if the form's data is
    invalid it will render the same page and form's data but with warnings.
    '''
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/'+username)
    else:
        return render(request, 'base.html', {
            'signupform':RegisterForm(),
            'loginform':form})

def LogOut(request):
    '''a logout view that logout the user if user is authenticated.'''
    if request.user.is_authenticated: logout(request)
    return redirect('MainPage')

# this loads all the timeline items to the ram, in this case it's a bad practice.
timeline_posts=TimelineItem.objects.all().order_by('-Date')
# i'm only working in local (my laptop) host right now (november 2017).
# so i don't know how to handle this with a big server.


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
