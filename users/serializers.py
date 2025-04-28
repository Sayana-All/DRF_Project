from rest_framework.serializers import ModelSerializer

from users.models import CustomUser, Payment


class PaymentSerializer(ModelSerializer):
    """Сериализатор для модели платежей"""

    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserSerializer(ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone", "city", "avatar"]
