from django.conf import settings
from django.db import models



User = settings.AUTH_USER_MODEL


class Contact(models.Model):
    # user        = models.ForeignKey(User, null=True, blank=True)
    username    = models.CharField(null=True,blank=True, max_length=255)
    email       = models.EmailField(null=True,blank=True, max_length=255)
    order_id    =models.CharField(null=True,blank=True, max_length=255)
    message     =models.TextField(null=True,blank=True, max_length=1000)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username)