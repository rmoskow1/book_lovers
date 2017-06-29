# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 20:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_books', '0005_book_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
