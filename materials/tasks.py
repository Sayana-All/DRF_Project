from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_course_update_email(user_email, course_title):
    """Задача для отправки письма подписчикам об обновлении курса"""
    send_mail(
        subject=f"Обновление курса: {course_title}",
        message=f"Курс '{course_title}' был обновлён. Посмотрите новые материалы.",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
