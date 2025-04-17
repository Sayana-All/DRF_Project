from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели курса"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели курса"""

    class Meta:
        model = Lesson
        fields = "__all__"
