from django.db import models
from django.conf import settings










class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    publisher = models.ForeignKey('Publisher', null=True, blank=True)

    def __str__(self):
        return self.user.__str__() + "'s profile"