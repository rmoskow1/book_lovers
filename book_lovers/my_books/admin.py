from django.contrib import admin
from .models import Publisher,Book,Tag,Profile



admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Profile)