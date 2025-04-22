from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Lesson, Course


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


class Payment(models.Model):
    """Модель для платежей пользователя"""

    CASH_PAY = "cash"
    TRANSFER_TO_ACCOUNT = "transfer"
    PAYMENT_METHOD_CHOICES = [
        (CASH_PAY, "наличные"),
        (TRANSFER_TO_ACCOUNT, "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        help_text="Укажите отправителя платежа",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    payment_date = models.DateTimeField(verbose_name="Дата оплаты", auto_now_add=True)

    paying_lesson = models.ForeignKey(
        Lesson,
        verbose_name="Оплата урока",
        help_text="Укажите оплаченный урок",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payment_lsn",
    )
    paying_course = models.ForeignKey(
        Course,
        verbose_name="Оплата курса",
        help_text="Укажите оплаченный курс",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payment_crs",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма платежа", help_text="Укажите сумму платежа")
    payment_method = models.CharField(
        max_length=8, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты", help_text="Выберите способ оплаты"
    )

    def __str__(self):
        return f"{self.user} - {self.payment_date} - {self.paying_lesson if self.paying_lesson else self.paying_course} - {self.payment_method} {self.payment_method}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-payment_date",)
