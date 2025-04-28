from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """Проверка, является ли пользователь модератором"""

    message = "Действие недоступно, так как вы не являетесь модератором"

    def has_permission(self, request, view):
         return request.user.groups.filter(name="Moder").exists()
