from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        unique=True,
        blank=False,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "username уже занят.",
        },
    )
    email = models.EmailField(
        verbose_name="email",
        max_length=254,
        blank=False,
        unique=True,
        error_messages={
            "unique": "Такой email уже зарегистрирован.",
        },
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
    )

    class Meta:
        db_table = "auth_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return f"{self.username}"
