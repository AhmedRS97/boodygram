from django.shortcuts import render, redirect, get_object_or_404

# importing the models
from .models import (  # a cleaner way to import.
    User, Post, Follow, TimelineItem
)
# importing the forms
from .forms import (  # a cleaner way to import.
    LoginForm, RegisterForm, ProfilePhoto, PostForm
)
from django.contrib.auth.decorators import login_required  # good decorator
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator # the good ol' paginator :D
from .miscellaneous import * # my custom miscellaneous functions
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse

# Create your views here.


def Register(request):
    """
    a Register view that validate a form's data and save it to database, then
    it authenticate and login the user and redirect to the user profile page.
    if the form's data is invalid it will render the same page and form's data
    but with warnings.
    """
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
            'signupform': form,
            'loginform': LoginForm()}, status=401)  # returning status 401 if form is invalid.


def Login(request):
    """
    a Login view that validates the form's data and authenticate and login the
    user and redirect the user to the profile page. if the form's data is
    invalid it will render the same page and form's data but with warnings.
    """
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
            'signupform': RegisterForm(),
            'loginform': form}, status=401)  # returning status 401 if form is invalid.


def LogOut(request):
    """a logout view that logout the user if user is authenticated."""
    if request.user.is_authenticated: logout(request)
    return redirect('MainPage')

# this loads all the timeline items to the ram, in this case it's a bad practice.
timeline_posts=TimelineItem.objects.all().order_by('-Date')
# i'm only working in local (my laptop) host right now (november 2017).
# so i don't know how to handle this with a big server.


def Timeline(request):
    """
    this view will read the timeline items from timeline_posts variable.
    then it append the timeline item's post to the posts_list variable if the
    user in the followers field. then it makes a paginator for posts_list, then
    it render 'user-home' template with the paginator object variable posts.
    """
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
    """
this function will handle both Get and Post requests. in Get requests it will
redirect the users if authenticated, otherwise, they will Get Signup/Login form.
In Post requests it will Create a user if the form has gender field. otherwise,
it will authenticate user if the Post have <= 3 fields and check for username &
password fields are found.. I think this approach is weak!!.
    """
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


class UserProfile(ListView, FormMixin):
    """
this view takes a request and username, the username argument is taken from the requested url.
this view will get the number of the user followers, followed and posts to use it to render user info, then it will
paginate the user posts list. if the user is authenticated it will check if the user is visiting his own profile,
else it will check if the user who made the request is following the requested user. finally all this variables will
sent as context data to the template.
NOTE: the template have UI logic in it, that it will show things differently.
    """
    form_class = ProfilePhoto
    paginate_by = 12
    context_object_name = 'posts'
    template_name = 'user/user-profile.html'

    def get(self, request, *args, **kwargs):
        self.object = None  # if this line deleted, it will cause an error
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)  # Explicitly states what get to call.

    @method_decorator(login_required(login_url='/'))  # using login_required function in method_decorator
    def post(self, request, *args, **kwargs):  # When the form is submitted, it will enter here
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            request.user.avatar = request.FILES['avatar']
            request.user.save()
            self.form = self.get_form(self.form_class)
        # Whether the form validates or not, the view will be rendered by get()
        return self.get(request, *args, **kwargs)

    def get_queryset(self):  # creating instance variable ref_user and return the user's posts.
        self.ref_user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(user=self.ref_user).order_by('-created')  # ordered by descending creation date

    def get_context_data(self, **kwargs):  # updating the context data
        context = super(UserProfile, self).get_context_data(**kwargs)  # getting context data Dict from the class.

        context.update({'posts_num': Post.objects.filter(user=self.ref_user).count(),  # counting posts
                        'following': Follow.objects.filter(follower=self.ref_user).count(),  # counting followed
                        'followers': Follow.objects.filter(followed=self.ref_user).count(),  # counting followers
                        'user': self.ref_user})  # adding the instance variable ref_user to context.
        if self.request.user.is_authenticated: context.update({  # updating context if user is authenticated.
            'same_user': self.request.user.username == self.ref_user.username,
            'is_followed': Follow.objects.filter(follower=self.request.user, followed=self.ref_user) if 'same_user' else None
        })
        return context


def FollowUser(request, username):
    """
this is view takes username argument from the url. it checks if the user is authenticated
then it query to find out if the user is not already following the target user,
if true it will create the follow object and then refresh the page.
    """
    if request.user.is_authenticated:
        followed= get_or_none(Follow,
            follower=request.user,followed=User.objects.get(username=username))
        if followed == None:
            Follow.objects.create(follower=request.user,
                followed=User.objects.get(username=username))
    return redirect('/'+username)

def UnfollowUser(request, username):
    """ it's the opposite of FollowUser view."""
    if request.user.is_authenticated:
        followed= get_or_none(Follow,
            follower=request.user,followed=User.objects.get(username=username))
        if followed != None:
            Follow.objects.get(follower=request.user,
                followed=User.objects.get(username=username)).delete()
    return redirect('/'+username)

@login_required(login_url='/') #the login_required decorator > will check if user is logged in
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
