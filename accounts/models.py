from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    phone_number = models.CharField(max_length=12, unique=True)
    profile_completed = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username
