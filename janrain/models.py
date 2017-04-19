from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class JanrainUser(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='janrain_user')
    username   = models.CharField(max_length=512, blank=False)
    provider   = models.CharField(max_length=64, blank=False)
    identifier = models.URLField(max_length=512, blank=False)
    avatar     = models.URLField(max_length=512, blank=True)
    url        = models.URLField(max_length=512, blank=True)
