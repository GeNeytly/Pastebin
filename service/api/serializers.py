from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from posts import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user."""

    class Meta:
        model = models.User
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the post."""

    created_at = serializers.DateTimeField(read_only=True)
    author = UserSerializer(read_only=True)
    is_public = serializers.SerializerMethodField(read_only=True)

    def get_is_public(self, instance):
        if self.context['request'].method == 'POST':
            return False
        return instance.is_public

    class Meta:
        model = models.Post
        fields = (
            'id',
            'title',
            'text',
            'created_at',
            'author',
            'tags',
            'is_public'
        )


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


class PostReportViewSerializer(serializers.ModelSerializer):
    """Serializer for the post without annotated field "is_public"."""

    created_at = serializers.DateTimeField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'text', 'created_at', 'author', 'tags')


class ReportViewSerializer(serializers.ModelSerializer):
    """The serializer responsible for the presentation of the report."""

    post = PostReportViewSerializer()

    class Meta:
        model = models.Report
        fields = ('id', 'post', 'expire_time')
