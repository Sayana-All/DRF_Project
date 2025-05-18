from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer, IsOwner

from .models import Course, Lesson, SubscribeUpdateCourse
from .paginations import CustomPagination
from .serializers import CourseSerializer, LessonSerializer
from .tasks import add_pr


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="description from swagger_auto_schema via method_decorator"),
)
class CourseViewSet(ModelViewSet):
    """Общий контроллер для модели курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

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

    def get_serializer_context(self):
        """Метод для добавления текущего пользователя в контекст"""
        context = super().get_serializer_context()
        context["request_user"] = self.request.user
        return context


class SubscribeToggleAPIView(APIView):
    """Контроллер для подписки/отписки пользователя от курса"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        course = get_object_or_404(Course, id=course_id)
        subs_item = SubscribeUpdateCourse.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            add_pr.delay()
            message = f"Подписка на курс {course} удалена"
        else:
            SubscribeUpdateCourse.objects.create(user=user, course=course, is_subscribe=True)
            add_pr.delay()
            message = f"Подписка на курс {course} добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


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
    pagination_class = CustomPagination


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
