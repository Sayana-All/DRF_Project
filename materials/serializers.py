from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoUrlValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса"""

    lessons_info = LessonSerializer(source="lessons", many=True, read_only=True)
    count_lessons = SerializerMethodField()

    @staticmethod
    def get_count_lessons(instance):
        """Метод для подсчета количества уроков"""

        if instance.lessons:
            return instance.lessons.count()
        return 0

    class Meta:
        model = Course
        fields = ["id", "title", "description", "owner", "preview", "count_lessons", "lessons_info"]
