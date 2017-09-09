# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 17:40
from __future__ import unicode_literals

from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model("posts", "Category")
    Category.objects.create(name="Python", description="As we are programming in python...")


def reverse(apps, schema_editor):
    Category = apps.get_model("posts", "Category")
    Category.objects.filter(name="Python").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories, reverse),
    ]
