from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """Общий контроллер для модели курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """Метод для автоматического назначения создателя курса его владельцем"""
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_permissions(self):
        """Метод для проверки прав пользователя"""
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModer,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Контроллер для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)

    def perform_create(self, serializer):
        """Метод для автоматического назначения создателя урока его владельцем"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """Контроллер для отображения списка доступных уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Контроллер для отображения подробностей урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    """Контроллер для редактирования урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    """Контроллер для удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner)
