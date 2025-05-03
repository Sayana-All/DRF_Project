from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson, SubscribeUpdateCourse
from materials.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoUrlValidator(field="video_url")]


class SubscribeUpdateCourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписки на обновления курса"""

    class Meta:
        model = SubscribeUpdateCourse
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курса"""

    lessons_info = LessonSerializer(source="lessons", many=True, read_only=True)
    count_lessons = SerializerMethodField()
    subscribe = SerializerMethodField()

    @staticmethod
    def get_count_lessons(instance):
        """Метод для подсчета количества уроков"""

        if instance.lessons:
            return instance.lessons.count()
        return 0

    def get_subscribe(self, instance):
        """Метод для проверки статуса подписки на обновления курса"""

        user = self.context.get("request_user")
        if user and not user.is_anonymous:
            return SubscribeUpdateCourse.objects.filter(user=user, course=instance, is_subscribe=True).exists()
        return False

    class Meta:
        model = Course
        fields = ["id", "title", "description", "owner", "subscribe", "preview", "count_lessons", "lessons_info"]
