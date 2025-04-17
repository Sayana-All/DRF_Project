from django.db import models


class Course(models.Model):
    """Класс для модели курса студентов"""

    title = models.CharField(max_length=100, verbose_name="Название", help_text="Укажите название курса")
    preview = models.ImageField(
        upload_to="course/preview/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для превью",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание", help_text="Введите описание курса")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """Класс для модели урока"""

    title = models.CharField(max_length=150, verbose_name="Название", help_text="Укажите название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание", help_text="Введите описание урока")
    course = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Укажите курс для урока",
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    preview = models.ImageField(
        upload_to="lesson/preview/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для превью",
    )
    video_url = models.URLField(verbose_name="Ссылка на видеоурок", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
