from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для профиля пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите адрес вашей почты")
    phone = models.CharField(
        max_length=30, verbose_name="Номер телефона", blank=True, null=True, help_text="Введите номер телефона"
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", blank=True, null=True, help_text="Укажите ваш город проживания"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите ваш аватар(изображение)",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
