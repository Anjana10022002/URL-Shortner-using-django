from django.db import models
from django.contrib.auth.models import User

class URLShortner(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    url = models.URLField()
    short_url = models.CharField(max_length=50, unique=True)
    time = models.DateTimeField(auto_now_add=True)

    