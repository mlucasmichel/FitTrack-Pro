from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model for FitTrack Pro.
    Allows for future expansion while maintaining compatibility with Django's authentication.
    """

    def __str__(self):
        return self.username
