from logging import Logger

from django.conf import settings
from django.db.models.expressions import Exists, OuterRef
from django.utils import timezone

from api import permissions
from api import serializers
from api.mixins import CacheMixin
from posts import models

logger = Logger(__name__)


class PostViewSet(CacheMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthor,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    cache_base_name = 'post'
    cache_obj_lifetime = settings.CACHE_LIFETIME

    def get_queryset(self):
        """Returns all the user's posts, with an annotated field "is_public",
        which means whether there is a report with this post."""
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
        """Call serializer.save() with param author=self.request.user."""
        serializer.save(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        logger.info(len(connection.queries))
        logger.info(connection.queries)
        return super().dispatch(request, *args, **kwargs)


class ReportViewsSet(CacheMixin):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (permissions.IsAuthorOrReadOnly,)
    cache_base_name = 'report'
    cache_obj_lifetime = settings.CACHE_LIFETIME

    def get_queryset(self):
        """Returns all reports that have not yet arrived expire time."""
        queryset = models.Report.objects.filter(
            expire_time__gte=timezone.now()
        ).select_related(
            'post__author'
        ).prefetch_related('post__tags')
        return queryset

    def get_serializer_class(self):
        """Returns ReportViewSerializer if request method
        is GET ReportCreateSerializer otherwise."""
        if self.request.method == 'GET':
            return serializers.ReportViewSerializer

        return serializers.ReportCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        logger.info(len(connection.queries))
        logger.info(connection.queries)
        return super().dispatch(request, *args, **kwargs)
