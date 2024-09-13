from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    mb_number_or_email = models.CharField(max_length=254, unique=True, blank=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Add unique related_name
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Add unique related_name
        blank=True,
    )

    def __str__(self):
        return self.email or self.username
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'mb_number_or_email': self.mb_number_or_email
        }
