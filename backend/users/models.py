from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHIOCE_ROLE = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    REQUIRED_FIELDS = ["email", "password"]
    confirmation_code = models.CharField(verbose_name='Код подтверждения',
                                         max_length=40, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == self.USER or self.role == self.MODERATOR:
            self.is_staff = False
        if self.role == self.ADMIN or self.is_superuser:
            self.is_staff = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)
