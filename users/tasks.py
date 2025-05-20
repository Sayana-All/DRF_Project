from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from users.models import CustomUser


@shared_task
def deactivate_inactive_users():
    """Задача по деактивации пользователей, не заходивших в приложение более месяца"""

    one_month_ago = timezone.now() - relativedelta(months=1)
    inactive_users = CustomUser.objects.filter(is_active=True, last_login__lt=one_month_ago)

    count = inactive_users.update(is_active=False)
    return f"{count} пользователей заблокировано за отсутствие активности"
