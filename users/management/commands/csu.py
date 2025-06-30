from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Команда для создания суперпользователя"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-existing", action="store_true", help="Пропускает команду, если суперпользователь уже создан"
        )

    def handle(self, *args, **options):
        email = "admin@sky.com"
        password = "qwerty25"  # Лучше вынести в переменные окружения!

        if options["skip_existing"] and CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Суперпользователь {email} уже существует, пропускаем"))
            return

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь {email} создан"))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Пользователь {email} уже существовал (но не был суперпользователем). Права обновлены"
                )
            )
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
