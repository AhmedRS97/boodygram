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

def Timeline(request):
    '''
    this view will read the timeline items from timeline_posts variable.
    then it append the timeline item's post to the posts_list variable if the
    user in the followers field. then it makes a paginator for posts_list, then
    it render 'user-home' template with the paginator object variable posts.
    '''
    posts_list=[x.post for x in timeline_posts if request.user in x.followers.all()]
    paginator = Paginator(posts_list, 18)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return render(request, 'user/user-home.html', {'posts':posts})

def MainPage(request):
    '''
this function will handle both Get and Post requests. in Get requests it will
redirect the users if authenticated, otherwise, they will Get Signup/Login form.
In Post requests it will Create a user if the form has gender field. otherwise,
it will authenticate user if the Post have <= 3 fields and check for username &
password fields are found.. I think this approach is weak!!.
    '''
    if request.method == "GET":
        if request.user.is_authenticated:
            return Timeline(request)
        else:
            return render(request, 'base.html', {
                'signupform':RegisterForm(),
                'loginform':LoginForm()})
    if request.method == "POST":
        if 'gender' in request.POST:
            return Register(request)
        if len(request.POST) <= 3 and 'username' in request.POST and 'password' in request.POST:
            return Login(request)
    return redirect('MainPage')

#@login_required #the login_required decorator > will check if user is logged in
def PostFormView(request, username):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = PostForm()
        if request.method == "POST":
            # request.FILES is for getting the attached images or files
            form = PostForm(request.POST, request.FILES)
            # checking if the Form data is valid.
            if form.is_valid():
                post = form.save(commit=False)
                post.user = User.objects.get(pk=request.user.pk)
                post.save()
                return redirect('MainPage') # redirects to MainPage url.

        return render(request, 'user/post-form.html', {'form':form})
    else:
        return redirect('MainPage') # redirects to MainPage url.
