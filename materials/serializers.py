from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели курса"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели курса"""

    lessons_info = LessonSerializer(source="lessons", many=True)
    count_lessons = SerializerMethodField()

    @staticmethod
    def get_count_lessons(instance):
        """Метод для подсчета количества уроков"""

        if instance.lessons:
            return instance.lessons.count()
        return 0

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "count_lessons", "lessons_info"]




#class CourseDetailSerializer(ModelSerializer):
#    """Сериализатор для отображения количества уроков в курсе"""
#
#
#    class Meta:
#        model = Course
#        fields = ["title", "count_lessons"]



