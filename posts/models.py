from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import re


class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    styles = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    DRAFT = 'DRF'
    PUBLISHED = 'PUB'
    DELETED = 'DEL'

    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (DELETED, 'Deleted')
    )

    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField()
    title = models.CharField(max_length=155)
    title_slug = models.CharField(max_length=155, null=True, blank=True)
    content = models.TextField()
    summary = models.CharField(max_length=155)
    category = models.ForeignKey(Category)
    media = models.TextField(null=True, blank=True)  # Use with an url until media model is included
    status = models.CharField(max_length=3, choices=STATUS, default=DRAFT)

    class Meta:
        unique_together = ('title', 'owner',)

    @staticmethod
    def generate_title_slug(source):
        source = source.lower()

        for string, replacement in settings.TITLE_SLUG_REPLACEMENTS:
            source = source.replace(string, replacement)
            
        return "-".join(re.findall("[a-zA-Z0-9]+", source))


class Comment(models.Model):
    owner = models.ForeignKey(User)
    content = models.TextField()
    post = models.ForeignKey(Post)

    created_at = models.DateTimeField(auto_now_add=True)  # automáticamente añada la fecha de creación
    modified_at = models.DateTimeField(auto_now=True)  # automáticamente actualiza la fecha al guardar

    def __str__(self):
        return "%s - %s" % (self.owner.username, self.post.title)


class FavoritePost(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)

    class Meta:
        unique_together = ('user', 'post')
