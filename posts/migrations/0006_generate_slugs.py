# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from posts.models import Post
from django.db import migrations


def generate_slugs(apps, schema_editor):
    posts = Post.objects.all()
    
    for post in posts:
        post.title_slug = Post.generate_title_slug(post.title)
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20171012_1207'),
    ]

    operations = [
        migrations.RunPython(generate_slugs),
    ]
