from pprint import pprint

from rest_framework.viewsets import ModelViewSet

from api import serializers
from posts.models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author').prefetch_related('tags')
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        res = super().dispatch(request, *args, **kwargs)
        pprint((len(connection.queries), "---------------------------"))
        pprint((connection.queries))
        return res
