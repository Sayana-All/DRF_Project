from django.http import HttpResponse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser, Payment
from users.serializers import CustomUserSerializer, PaymentSerializer
from users.services import create_stripe_price, create_stripe_session


class CustomUserCreateAPIView(CreateAPIView):
    """Контроллер для регистрации пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод для проверки авторизованных пользователей"""
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

    def perform_create(self, serializer):
        """Метод для исполнения оплаты через сервис платежей Stripe"""

        user = self.request.user
        user.save()
        payment = serializer.save(user=user)
        price = create_stripe_price(payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentUpdateAPIView(UpdateAPIView):
    """Контроллер для редактирования платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyAPIView(DestroyAPIView):
    """Контроллер для удаления платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SuccessPaymentView(View):
    """Контроллер для подтверждения успешной оплаты"""

    def get(self, request, *args, **kwargs):
        return HttpResponse("Ваш платеж прошел успешно. Спасибо за оплату!")
