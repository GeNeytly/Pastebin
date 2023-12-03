from rest_framework import serializers

from posts import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'text', 'created_at', 'author', 'tags')


