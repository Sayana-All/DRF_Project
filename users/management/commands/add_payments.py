from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import CustomUser, Payment


class Command(BaseCommand):
    help = "Добавление данных платежей в БД"

    def handle(self, *args, **options):
        user1, _ = CustomUser.objects.get_or_create(
            email="ivan-ivanov@example.com",
            defaults={"first_name": "Иван", "last_name": "Иванов"}
        )
        user1.set_password("qwerty25")
        user1.save()
        user2, _ = CustomUser.objects.get_or_create(
            email="petr-petrov@example.com",
            defaults={"first_name": "Петр", "last_name": "Петров"}
        )
        user2.set_password("qwerty45")
        user2.save()

        course1, _ = Course.objects.get_or_create(
            title="Курс Python-разработчик",
            defaults={"description": "Популярный курс для бакэндеров"}
        )
        course1.save()
        course2, _ = Course.objects.get_or_create(
            title="Курс Java-разработчик",
            defaults={"description": "Популярный курс для фронтендов"}
        )
        course2.save()

        lesson1, _ = Lesson.objects.get_or_create(
            title="Основы программирования",
            defaults={"description": "Урок для начинающих по базовому программированию", "course": course1}
        )
        lesson1.save()
        lesson2, _ = Lesson.objects.get_or_create(
            title="Типы данных",
            defaults={"description": "Простые переменные данных и их виды", "course": course1}
        )
        lesson2.save()

        payments = [
            {"user": user1, "paying_lesson": lesson1, "payment_method": Payment.CASH_PAY, "amount": 3000},
            {"user": user1, "paying_lesson": lesson2, "payment_method": Payment.CASH_PAY, "amount": 2500},
            {"user": user2, "paying_course": course2, "payment_method": Payment.TRANSFER_TO_ACCOUNT, "amount": 50000},
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Платёж от {payment.user.email} на сумму {payment.amount} успешно добавлен"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"⚠Платёж от {payment.user.email} на сумму {payment.amount} уже существует"
                ))
