import time
from logging import Logger

from django.conf import settings
from django.core.cache import cache
from django.db.models.expressions import Exists, OuterRef
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api import permissions
from api import serializers
from posts import models

logger = Logger(__name__)


class AbstractCachedViewSet(ModelViewSet):
    """An abstract class with redefined
    methods for working with the cache."""

    # it will work with a cache that has a
    # name f'{cache_base_name}_cache/{obj_id}'
    cache_base_name = None

    def retrieve(self, request, *args, **kwargs):
        """Retrieve the model instance, sets the cache with
        the serializer data value, if there is none."""
        obj_cache_name = f'{self.cache_base_name}_cache/{kwargs["pk"]}'
        obj_data = cache.get(obj_cache_name)
        if not obj_data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            obj_data = serializer.data
            cache.set(obj_cache_name, obj_data, settings.CACHE_LIFETIME)
        return Response(obj_data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Partial update the model instance and invalidates the cache."""
        obj_cache_name = f'{self.cache_base_name}_cache/{kwargs["pk"]}'
        cache.delete(obj_cache_name)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Destroy  the model instance and invalidates the cache."""
        obj_cache_name = f'{self.cache_base_name}_cache/{kwargs["pk"]}'
        cache.delete(obj_cache_name)
        return super().destroy(request, *args, **kwargs)


class PostViewSet(AbstractCachedViewSet):
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthor,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    cache_base_name = 'post'

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


class ReportViewsSet(AbstractCachedViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (permissions.IsAuthorOrReadOnly,)
    cache_base_name = 'report'

    def get_queryset(self):
        """Returns all reports that have not yet arrived expire time"""
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
