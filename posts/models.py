from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    styles = models.TextField(null=True, blank=True)


class Post(models.Model):
    DRAFT = 'DRF'
    PUBLISHED = 'PUB'

    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField()
    title = models.CharField(max_length=155)
    subtitle = models.CharField(max_length=155)
    content = models.TextField()
    summary = models.CharField(max_length=155)
    category = models.ForeignKey(Category)
    media = models.TextField(null=True, blank=True)  # Use with an url until media model is included
    status = models.CharField(max_length=3, choices=STATUS, default=DRAFT)
