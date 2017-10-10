"""wellcoders_backend URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from posts.api import PostsAPI, UserPostList
from users.api import Register, PasswordResetView
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register("posts", PostsAPI, base_name="posts_api")

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/1.0/', include(router.urls)),
    url(r'^api/1.0/login/', obtain_jwt_token),
    url(r'^api/1.0/register/', Register.as_view(), name='register'),
    url(r'^api/1.0/(?P<username>[0-9a-zA-Z_-]+)/posts/$', UserPostList.as_view(), name='userpost-list'),
    url(r'^api/1.0/password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
    # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
    #url(r'^api/1.0/password/change/$', UpdatePassword.as_view(), name='rest_password_change'),
]
