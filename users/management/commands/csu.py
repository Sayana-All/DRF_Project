from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Команда для создания суперпользователя"

    def handle(self, *args, **kwargs):
        user, created = CustomUser.objects.get_or_create(
            email="admin@sky.com",
            defaults={
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            }
        )
        user.set_password("qwerty25")
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {user.email} создан'))
        else:
            self.stdout.write(self.style.WARNING(f'Суперпользователь {user.email} уже существует'))
