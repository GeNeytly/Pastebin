import logging
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from posts import models


logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user."""
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the post."""
    created_at = serializers.DateTimeField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'text', 'created_at', 'author', 'tags')


class ReportCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a report."""
    class Meta:
        model = models.Report
        fields = ('id', 'post', 'expire_time')

    def validate_post(self, post):
        """Checks that the author of the report and
        the author of the post are the same person.
        """
        if post.author != self.context['request'].user:
            raise ValidationError(
                'You cannot create a report with a post by another author!'
            )
        return post

    def validate_expire_time(self, value):
        """Checks the expire time is longer than the current one."""
        if value < timezone.now() + timedelta(minutes=2):
            raise ValidationError(
                'You cannot create a report with expire time than now!'
            )
        return value


class ReportViewSerializer(serializers.ModelSerializer):
    """The serializer responsible for the presentation of the report."""
    post = PostSerializer()

    class Meta:
        model = models.Report
        fields = ('id', 'post', 'expire_time')
