from django.db import models
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='client_set',  # 这里添加 related_name 参数
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='client_set',  # 这里添加 related_name 参数
        blank=True,
    )

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
