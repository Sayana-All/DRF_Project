from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course, SubscribeUpdateCourse


@shared_task
def send_course_update_email(course_id):
    """Задача для отправки письма подписчикам об обновлении курса"""

    course = Course.objects.get(id=course_id)
    subscribers = SubscribeUpdateCourse.objects.filter(course=course, is_subscribe=True)

    for subscription in subscribers:
        user = subscription.user
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message=f"Курс '{course.title}' был обновлён. Посмотрите новые материалы.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
