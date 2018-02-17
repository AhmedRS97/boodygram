"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url#, include
from django.contrib import admin
from instagram.apps.core import views
from django.conf import settings

app_name = 'core'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.MainPage, name="MainPage"),
    url(r'^signup/$', views.signup, name='Signup'),
    url(r'^signin/$', views.signin, name="Signin"),
    url(r'^logout/$', views.LogOut, name="LogOut"),
    url(r'^(?P<username>[\w.]+)/follow/', views.FollowUser, name='FollowUser'),
    url(r'^(?P<username>[\w.]+)/unfollow/', views.UnfollowUser, name='UnfollowUser'),
    url(r'^(?P<username>[\w.]+)/$', views.UserProfile.as_view(), name="UserProfile"),
    #url(r'^(?P<username>[\w.]+)/p/(?P<post_id>[\d]+)$', views.UserPost, name='UserPost'),
    url(r'^(?P<username>[\w.]+)/post/$', views.PostFormView, name="PostFormView"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
