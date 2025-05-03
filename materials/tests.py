from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, SubscribeUpdateCourse
from users.models import CustomUser


class CourseTestCase(APITestCase):
    """Класс для тестирования CRUD курсов"""

    def setUp(self):
        """Метод для получения тестовых данных"""
        self.user = CustomUser.objects.create(email="test@admin.com")
        self.course = Course.objects.create(title="Тестовый курс", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тестирование для просмотра одного курса"""
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        """Тест на создание курса"""
        url = reverse("materials:course-list")
        data = {
            "title": "Новый курс"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """Тест по редактированию курса"""
        url = reverse("materials:course-detail", args=[self.course.pk])
        data = {"title": "Измененный курс"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Измененный курс")

    def test_course_delete(self):
        """Тест на удаление курса"""
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """Тест на отображение списка курса"""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.course.pk,
                    'title': self.course.title,
                    'description': None,
                    'owner': self.user.pk,
                    'subscribe': False,
                    'preview': None,
                    'count_lessons': 0,
                    'lessons_info': []
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):
    """Класс для тестирования CRUD уроков"""

    def setUp(self):
        """Метод для получения тестовых данных"""
        self.user = CustomUser.objects.create(email="test@admin.com")
        self.course = Course.objects.create(title="Тестовый курс", owner=self.user)
        self.lesson = Lesson.objects.create(title="Тестовый урок", description="Пробное описание", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование для просмотра одного урока"""
        url = reverse("materials:lesson_detail", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)
        self.assertEqual(data.get("description"), self.lesson.description)

    def test_lesson_create(self):
        """Тест на создание урока"""
        url = reverse("materials:create")
        data = {
            "title": "Новый урок"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест по редактированию урока"""
        url = reverse("materials:lesson_edit", args=[self.lesson.pk])
        data = {"title": "Измененный урок"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Измененный урок")

    def test_lesson_delete(self):
        """Тест на удаление урока"""
        url = reverse("materials:lesson_delete", args=[self.lesson.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест на отображение списка уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'title': self.lesson.title,
                    'description': self.lesson.description,
                    'preview': None,
                    'video_url': None,
                    'course': self.course.pk,
                    'owner': self.user.pk,
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)



class SubscribeTestCase(APITestCase):
    """Класс для тестирования подписки на обновления курса"""

    def setUp(self):
        """Метод для получения тестовых данных"""
        self.user = CustomUser.objects.create(email="test@user.com")
        self.course = Course.objects.create(title="Курс по Django", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_add(self):
        """Тест добавления подписки"""
        url = reverse("materials:subscribe-toggle")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            SubscribeUpdateCourse.objects.filter(user=self.user, course=self.course, is_subscribe=True).exists()
        )
        self.assertEqual(response.data["message"], f"Подписка на курс {self.course.title} добавлена")

    def test_subscribe_remove(self):
        """Тест удаления подписки"""
        SubscribeUpdateCourse.objects.create(user=self.user, course=self.course, is_subscribe=True)

        url = reverse("materials:subscribe-toggle")
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            SubscribeUpdateCourse.objects.filter(user=self.user, course=self.course, is_subscribe=True).exists()
        )
        self.assertEqual(response.data["message"], f"Подписка на курс {self.course.title} удалена")
