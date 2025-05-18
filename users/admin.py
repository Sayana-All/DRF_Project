from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Класс пользователей для админки"""

    list_filter = ("id", "email")
    list_display = ("id", "email")
