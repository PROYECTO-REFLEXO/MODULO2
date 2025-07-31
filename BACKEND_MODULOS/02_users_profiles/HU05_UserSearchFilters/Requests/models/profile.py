# HU05_UserSearchFilters/models/profile.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    documento = models.CharField(max_length=50, unique=True)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} - {self.rol}'
