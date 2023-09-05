from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Модель User."""

    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Такой username уже занят.",
        },
    )
    email = models.EmailField(
        verbose_name="email",
        max_length=254,
        blank=False,
        unique=True,
        null=False,
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
        ordering = ("id",)

    def __str__(self):
        return f"{self.username}"


class Follow(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="following",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f"{self.user} подписан на {self.author}"
