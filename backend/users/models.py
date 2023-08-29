from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

import core.constants as const


class UserManager(BaseUserManager):
    """ Создает и возвращает пользователя с емэйлом, паролем и именем. """
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Имя пользователя обязательно.')

        if email is None:
            raise TypeError('Электронная почта обязательна.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Нужно обязательно указать пароль.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    email = models.EmailField(
        ('email address'),
        max_length=const.FIELD_LENGTH_254,
        unique=True,
        verbose_name='e-mail пользователя',
        error_messages={
            'unique': ("Такой e-mail уже используеется другим пользователем."),
        },
    )
    username = models.CharField(
        max_length=const.FIELD_LENGTH_150,
        unique=True,
        verbose_name='логин пользователя',
        error_messages={
            'unique': ("Пользователь с таким логином уже существует."),
        },
    )
    first_name = models.CharField(
        max_length=const.FIELD_LENGTH_150,
        blank=True
    )
    last_name = models.CharField(
        max_length=const.FIELD_LENGTH_150,
        blank=True
    )

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        unique_together = ('username', 'email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscribe(models.Model):
    siteuser = models.ForeignKey(
        User,
        related_name='subscribes',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE,
        verbose_name='Подписка на автора'
    )

    class Meta:
        unique_together = ('siteuser', 'author',)

    @property
    def is_owner(self, user):
        return self.siteuser == user
