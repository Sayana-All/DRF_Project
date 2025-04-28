from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser, Payment
from users.serializers import CustomUserSerializer, PaymentSerializer


class CustomUserCreateAPIView(CreateAPIView):
    """Контроллер для регистрации пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод для переопределения регистрации по email"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(ListAPIView):
    """Контроллер для отображения списка платежей"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paying_lesson", "paying_course", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentRetrieveAPIView(RetrieveAPIView):
    """Контроллер для отображения деталей платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentCreateAPIView(CreateAPIView):
    """Контроллер для создания платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(UpdateAPIView):
    """Контроллер для редактирования платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyAPIView(DestroyAPIView):
    """Контроллер для удаления платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
