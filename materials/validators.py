from rest_framework.serializers import ValidationError


class VideoUrlValidator:
    """Валидатор для проверки ссылки на видеоурок"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value and "youtube.com" not in tmp_value:
            raise ValidationError(f"{tmp_value} является недопустимой ссылкой на видеоурок. Используйте контент с Youtube.")
