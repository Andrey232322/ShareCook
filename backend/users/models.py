from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True,)
    password = models.CharField(
        max_length=150,
        blank=False,
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'password')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
