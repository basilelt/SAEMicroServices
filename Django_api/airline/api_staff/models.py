from django.db import models
from django.contrib.auth.models import AbstractUser

class Staff(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='staff_set',  # 这里添加 related_name 参数
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='staff_set',  # 这里添加 related_name 参数
        blank=True,
    )

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff'



class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return self.flight_number