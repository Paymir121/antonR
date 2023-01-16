from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Group, Post, Follow, Comment, Like, Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title_post',
        'text',
        'pub_date',
        'author',
        'group',
        'image',
    )

    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        'pk',
        'title',
        'slug',
    )

    empty_value_display = '-пусто-'



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'post',
        'get_image',
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')
    empty_value_display = '-пусто-'
