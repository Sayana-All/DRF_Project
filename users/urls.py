from django.urls import path

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentDestroyAPIView, PaymentListAPIView, PaymentRetrieveAPIView,
                         PaymentUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment_detail"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payments_create"),
    path("payments/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name="payments_edit"),
    path("payments/<int:pk>/delete/", PaymentDestroyAPIView.as_view(), name="payments_delete"),
]
