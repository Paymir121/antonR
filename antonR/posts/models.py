from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreatedModel
from django.db.models import Count


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class PostManager(models.Manager):
    def post_liked(self):
        return self.annotate(
            counter_like=Count('liked')).order_by('-counter_like')


class Post(models.Model):
    title_post = models.CharField(
        max_length=200,
        null=True,
        blank=True,)
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Тип проекта',
        help_text='Тип проекта'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True,
    )
    objects = models.Manager()
    post_obj = PostManager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментарий',
        help_text='комментарий к которой будет относиться пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор коментария'
    )
    text = models.TextField(
        'Текст коментария',
        help_text='Введите текст коментария'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарий'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = [['author', 'user']]

    def __str__(self) -> str:
        return f'{self.author}'


class Like(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='liked',
        verbose_name='Лайк Посту',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author_like",
        verbose_name='Автор лайка'
    )

    class Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'
        unique_together = [['post', 'author']]


class Image(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Картинка К Посту',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True,
    )
    text = models.TextField(
        'Описание картинки',
        help_text='текст под картинкой'
    )

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
        unique_together = [['post', 'image']]
