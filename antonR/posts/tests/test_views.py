from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.core.cache import cache

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        cache.clear()
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_index_page_show_correct_context(self):
        """на index правильная информацйия."""
        response = self.authorized_client.get(reverse('posts:index'))
        post = response.context['page_obj'][0]
        self.assertEqual(post.text, 'Тестовый пост')
        self.assertEqual(post.author.username, 'auth')
        self.assertEqual(post.group.title, 'Тестовая группа')

    def test_index_cache(self):
        """Тетсирование кеширования главной страницы."""
        new_post = Post.objects.create(
            author=self.user,
            text='New Тестовый пост ',
            group=self.group
        )
        index_with_posts = self.authorized_client.get(
            reverse(
                'posts:index')).content
        new_post.delete()

        index_without_posts = self.authorized_client.get(
            reverse('posts:index')).content
        self.assertEqual(index_with_posts, index_without_posts)

        cache.clear()
        index_clear_cashe = self.authorized_client.get(
            reverse(
                'posts:index')).content
        self.assertNotEqual(index_clear_cashe, index_with_posts)

    def test_pages_uses_correct_template(self):
        """View URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',

            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}):
            'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': self.user.username}):
            'posts/profile.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
            'posts/post_create.html',
        }
        # Проверяем, что при обращении
        # к name вызывается соответствующий HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class PostPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_name')
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug='test_slug',
            description='Тестовое описание',
        )
        for count_post in range(18):
            cls.post = Post.objects.create(
                text='Тестовый текст',
                author=cls.user,
                group=cls.group
            )

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index'),
            'posts:group_list': reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTests.group.slug}),
            'posts:profile': reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTests.user.username}),
        }
        for view, context_page in paginator_list.items():
            with self.subTest(f'{view}'):
                response = self.guest_client.get(context_page)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index') + '?page=2',
            'posts:group_list': reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTests.group.slug}) + '?page=2',
            'posts:profile': reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTests.user.username})
            + '?page=2',
        }
        for view, context_page in paginator_list.items():
            with self.subTest(f'{view}'):
                response = self.guest_client.get(context_page)
                self.assertEqual(len(response.context['page_obj']), 8)
