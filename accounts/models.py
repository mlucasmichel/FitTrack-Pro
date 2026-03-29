from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model for FitTrack Pro.
    Stores core user data and fitness goals.
    """
    # Daily Goals
    calorie_goal = models.PositiveIntegerField(default=2500)
    protein_goal = models.PositiveIntegerField(default=150)
    carbs_goal = models.PositiveIntegerField(default=300)
    fat_goal = models.PositiveIntegerField(default=80)

    def __str__(self):
        return self.username
