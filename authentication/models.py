
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_valid_until = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
