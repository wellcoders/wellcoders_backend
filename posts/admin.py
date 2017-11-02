from django.contrib import admin

# Register your models here.
from posts.models import Category, Post, FavoritePost

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(FavoritePost)
