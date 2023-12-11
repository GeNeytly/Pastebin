from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from api import serializers
from api.tests import test_data as td
from posts import models


class TestUserSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user1_data = td.create_user_data('mixin1')
        cls.user1 = models.User.objects.create(**user1_data)
        cls.serializer_cls = serializers.UserSerializer

    def test_user_serializer(self):
        """The data is serialize correctly."""
        serializers_data = self.serializer_cls(self.user1).data
        expected_data = {
            'id': self.user1.id,
            'username': self.user1.username,
            'email': self.user1.email

        }

        self.assertEqual(expected_data, serializers_data)


# class TestPostSerializers(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#
#         user1_data = td.create_user_data('mixin1')
#         cls.user1 = models.User.objects.create(**user1_data)
#         tag1_data = td.create_tag_data('mixin1')
#         cls.tag1 = models.Tag.objects.create(**tag1_data)
#         post1_data = td.create_post_data('mixin1', cls.user1)
#         cls.utc_now = datetime.utcnow()
#         post1_data['created_at'] = cls.utc_now
#         cls.post1 = models.Post.objects.create(**post1_data)
#         cls.post1.tags.set([cls.tag1])
#         cls.serializer_cls = serializers.PostSerializer
#
#     def test_post_serializer_with_post(self):
#         """Checks that the sterilizer returns the correct fields
#         with the post method"""
#         context = {'request': FakeRequest(method='POST')}
#         serializer = self.serializer_cls(self.post1, context=context)
#         expected_data = {
#             'id': self.post1.id,
#             'title': self.post1.title,
#             'text':  self.post1.text,
#             'created_at': self.utc_now.isoformat(),
#             'author': serializers.UserSerializer(self.user1).data,
#             'tags': self.post1.tags,
#             'is_public': False
#         }
#
#         self.assertEqual(expected_data, serializer.data)


