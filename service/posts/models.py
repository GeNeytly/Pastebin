from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='name of the tag',
        max_length=200,
        unique=True,

    )
    description = models.TextField(verbose_name='description of tag')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='title of the post', max_length=200)
    text = models.TextField(verbose_name='text of the post')
    created_at = models.DateTimeField(
        verbose_name='post creation date',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='author of the post'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='related tags of the post'
    )

    def __str__(self):
        return self.title


class Report(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='post that the author is sharing'
    )
    expire_time = models.DateTimeField(
        verbose_name='when the post will no longer be available'
    )
