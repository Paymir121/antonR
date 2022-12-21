from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост больше 15 буковок, а должно быть меньше',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_models_have_correct_group_names(self):
        """Проверяем, что у моделей корректно работает  название группы."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_models_have_correct_help_text(self):
        """Проверяем, что у моделей корректно работает  название группы."""
        group = PostModelTest.group
        self.assertEqual(group.description, 'Тестовое описание')

    def test_models_have_correct_verbose_name(self):
        """Проверяем, что у моделей корректно работает  название группы."""
        group = PostModelTest.group
        verbose_name = group.slug
        self.assertEqual(verbose_name, 'Тестовый слаг')
