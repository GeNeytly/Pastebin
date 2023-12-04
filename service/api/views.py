import logging
from pprint import pprint
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from api import serializers
from posts import models


logger = logging.getLogger(__name__)


class PostViewSet(ModelViewSet):
    queryset = models.Post.objects.select_related('author').prefetch_related('tags')
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        res = super().dispatch(request, *args, **kwargs)
        pprint((len(connection.queries), "---------------------------"))
        pprint((connection.queries))
        logger.debug('POOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOST')
        logger.debug((len(connection.queries)))
        logger.debug(connection.queries)
        return res


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

    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        res = super().dispatch(request, *args, **kwargs)
        logger.debug(connection.queries)
        return res
