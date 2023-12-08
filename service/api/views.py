from pprint import pprint
from logging import Logger

from django.db.models.expressions import Exists, OuterRef
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from api import serializers
from posts import models


logger = Logger(__name__)


class PostViewSet(ModelViewSet):
    # queryset = models.Post.objects.select_related(
    #     'author'
    # ).prefetch_related(
    #     'tags'
    # )
    #
    #     #
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        queryset = models.Post.objects.select_related(
            'author'
        ).prefetch_related(
            'tags'
        ).filter(
            author=self.request.user
        ).annotate(
            is_public=Exists(
                models.Report.objects.filter(post=OuterRef('id'))
            )
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        logger.info(len(connection.queries))
        logger.info(connection.queries)
        return super().dispatch(request, *args, **kwargs)


class ReportViewsSet(ModelViewSet):
    queryset = models.Report.objects.filter(
        expire_time__gte=timezone.now()
    ).select_related(
        'post__author'
    ).prefetch_related('post__tags')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ReportViewSerializer

        return serializers.ReportCreateSerializer

    def list(self, request, *args, **kwargs):
        pprint(request)
        return super().list(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        print(len(connection.queries))
        print(connection.queries)
        return super().dispatch(request, *args, **kwargs)