import shutil
import tempfile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


from ..models import Group, Post, Comment, Follow

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug_slug',
            description='Тестовое описание',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            image=uploaded
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text="Комментарий 1",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_post_create_form(self):
        """Posts.Forms. Создание нового Post."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small_new.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Текст поста новый',
            'group': self.group.id,
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        new_posts = Post.objects.first()
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username}),
        )
        self.assertEqual(new_posts.text, 'Текст поста новый')
        self.assertEqual(new_posts.image, 'posts/small_new.gif')
        self.assertEqual(new_posts.author.username, self.user.username)
        self.assertEqual(new_posts.group, self.group)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post_edit_form(self):
        """Posts.Forms. Можно редактировать посты."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'New Текст поста',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True
        )
        post_edit = Post.objects.get(id=self.post.id)
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={"post_id": self.post.id}))
        self.assertEqual(post_edit.text, 'New Текст поста')
        self.assertEqual(post_edit.group, self.group)
        self.assertEqual(post_edit.author.username, self.user.username)
        self.assertEqual(posts_count, Post.objects.count())

    def test_context_post_with_image(self):
        """тест на проверку картинки в post detail"""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        post = response.context['post']
        self.assertEqual(post.text, 'Тестовый пост')
        self.assertEqual(post.group, self.group)
        self.assertEqual(post.image, 'posts/small.gif')

    def test_context_page_with_image(self):
        """тест на проверку картинки """
        templates_url_names = {
            'posts:group_list': {'slug': self.group.slug},
            'posts:profile': {'username': self.user.username},
            'posts:index': ''
        }
        for address, var in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(
                    reverse(address, kwargs=var))
                post = response.context['page_obj'][0]
                self.assertEqual(post.text, 'Тестовый пост')
                self.assertEqual(post.group, self.group)
                self.assertEqual(post.image, 'posts/small.gif')

    def test_add_comment_for_author(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Комментарий 2',
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        new_comment = Comment.objects.get(id=(comment_count + 1))
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
        )
        self.assertEqual(new_comment.text, 'Комментарий 2')
        self.assertEqual(Comment.objects.count(), new_comment.id)


class FollowFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.first_user = User.objects.create_user(username='follower')
        cls.second_user = User.objects.create_user(username='following')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.first_user,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.post_second = Post.objects.create(
            author=cls.second_user,
            text='Тестовый пост',
            group=cls.group,
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.first_user)

    def test_url_follow(self):
        """Авторизованный пользователь может подписаться"""
        follow_url = reverse(
            'posts:profile_follow',
            kwargs={'username': self.first_user.username}
        )
        response = self.authorized_client.post(follow_url, follow=True)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_url_unfollow(self):
        """Авторизованный пользователь может отписаться"""
        Follow.objects.get_or_create(
            user=self.first_user,
            author=self.second_user
        )
        unfollow_url = reverse(
            'posts:profile_unfollow',
            kwargs={'username': self.second_user}
        )
        self.authorized_client.get(unfollow_url)
        self.assertFalse(
            Follow.objects.filter(
                user=self.first_user,
                author=self.second_user,
            ).exists()
        )

    def test_context_for_unfollow(self):
        """Авторизованный пользователь не видит подписки других людей"""
        Follow.objects.get_or_create(
            user=self.second_user,
            author=self.first_user
        )
        follow_url = reverse(
            'posts:follow_index'
        )
        response = self.authorized_client.post(follow_url, follow=True)
        self.assertEqual(len(response.context['page_obj']), 0)
