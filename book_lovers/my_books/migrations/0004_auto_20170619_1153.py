# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_books', '0003_auto_20170619_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tagged_books', to='my_books.Tag'),
        ),
    ]