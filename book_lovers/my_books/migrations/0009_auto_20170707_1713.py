# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 21:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_books', '0008_auto_20170706_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='owner',
        ),
        migrations.AddField(
            model_name='book',
            name='isVerified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='book',
            name='pen_name',
            field=models.CharField(default='Bartholomew the Jew', max_length=100, verbose_name='author name'),
        ),
        migrations.AddField(
            model_name='book',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='authored_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='users_who_favorite',
            field=models.ManyToManyField(blank=True, related_name='fav_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
