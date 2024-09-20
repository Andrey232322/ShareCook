from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
<<<<<<< HEAD
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
=======

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

>>>>>>> work
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'password')

    class Meta:
<<<<<<< HEAD
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
=======
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='подписчик'
>>>>>>> work
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
<<<<<<< HEAD
        related_name='following',
    )

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
=======
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
>>>>>>> work
