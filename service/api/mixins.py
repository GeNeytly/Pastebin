from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class RetrieveCacheMixin(ModelViewSet):
    """An mixin class with redefined retrieve
     method for working with the cache."""

    cache_base_name = None
    cache_obj_lifetime = None

    def retrieve(self, request, *args, **kwargs):
        """Retrieve the model instance, sets the cache with
        the serializer data value, if there is none."""
        obj_cache_name = f'{self.cache_base_name}_cache/{kwargs["pk"]}'
        obj_data = cache.get(obj_cache_name)
        if obj_data is None:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            obj_data = serializer.data
            cache.set(obj_cache_name, obj_data, self.cache_obj_lifetime)
        return Response(obj_data, status=status.HTTP_200_OK)


class PatchCacheMixin(ModelViewSet):
    """An mixin class with redefined partial_update
     method for working with the cache."""

    cache_base_name = None

    def partial_update(self, request, *args, **kwargs):
        """Partial update the model instance and invalidates the cache."""
        obj_cache_name = f'{self.cache_base_name}_cache/{kwargs["pk"]}'
        cache.delete(obj_cache_name)
        return super().partial_update(request, *args, **kwargs)


class DestroyCacheMixin(ModelViewSet):
    """An mixin class with redefined destroy
     method for working with the cache."""

    cache_base_name = None

    def destroy(self, request, *args, **kwargs):
        """Destroy  the model instance and invalidates the cache."""
        obj_cache_name = f'{self.cache_base_name}_cache/{kwargs["pk"]}'
        cache.delete(obj_cache_name)
        return super().destroy(request, *args, **kwargs)


class CacheMixin(RetrieveCacheMixin, PatchCacheMixin, DestroyCacheMixin):
    """An mixin class with redefined
    methods for working with the cache."""
