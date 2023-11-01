from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    title = models.CharField(verbose_name='Title of the post', max_length=200)
    text = models.TextField(verbose_name='Text of the post')
    created_at = models.DateTimeField(
        verbose_name='Post creation date',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author of the post'
    )

    def __str__(self):
        return self.title
