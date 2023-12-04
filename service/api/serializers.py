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


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = ('id', 'post', 'expire_time')


class ReportViewSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    curr_time = serializers.DateTimeField()

    class Meta:
        model = models.Report
        fields = ('id', 'post', 'expire_time', 'curr_time')
