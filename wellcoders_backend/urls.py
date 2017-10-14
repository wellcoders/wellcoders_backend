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
from posts.api import PostsAPI, UserPostList, CategoryList, CategoryPostList, CommentsAPI
from users.api import Register, UserAPI, Recovery
from media.api import MediaUploadViewSet

router = routers.DefaultRouter()
router.register("posts", PostsAPI, base_name="posts_api")
router.register("users", UserAPI, base_name="user_api")
router.register("comments", CommentsAPI, base_name="comments_api")
router.register("media", MediaUploadViewSet, base_name="media_api")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/1.0/', include(router.urls)),
    url(r'^api/1.0/login/', obtain_jwt_token),
    url(r'^api/1.0/register/', Register.as_view(), name='register'),
    url(r'^api/1.0/recovery/', Recovery.as_view(), name='recovery'),
    url(r'^api/1.0/categories/', CategoryList.as_view(), name='category'),
    url(r'^api/1.0/(?P<username>[0-9a-zA-Z_-]+)/$', UserPostList.as_view(), name='userpost-list'),
    url(r'^api/1.0/tag/(?P<category>[0-9a-zA-Z_-]+)/$', CategoryPostList.as_view(), name='categorypost-list')
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()