import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(amount):
    """Функция для создания цены в платежном сервисе stripe"""

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Функция для создания ссылки на оплату в stripe"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/payment-success/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
