from django.shortcuts import render, redirect
from .models import * # importing the models
from .forms import * # importing the forms
from django.contrib.auth.decorators import login_required #good decorator
from django.contrib.auth import authenticate, login, logout

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
