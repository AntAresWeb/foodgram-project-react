from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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
        max_length=254,
        unique=True,
        error_messages={
            'unique': ("Такой e-mail уже используеется другим пользователем."),
        },
    )

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('-id',)
        unique_together = ('username', 'email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)
