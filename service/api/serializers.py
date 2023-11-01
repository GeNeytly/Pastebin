from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('title', 'text', 'created_at', 'author')

