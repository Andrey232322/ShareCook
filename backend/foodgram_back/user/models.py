from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    is_subscribed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

