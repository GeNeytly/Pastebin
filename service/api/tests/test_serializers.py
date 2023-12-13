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
        cls.user_serializer = serializers.UserSerializer

    def test_contains_expected_fields(self):
        """The serializer contains all the necessary fields."""
        serializer = self.user_serializer(self.user1)
        expected_fields = {'id', 'email', 'username'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_id_field_content(self):
        """The serializer handles the instance.id field correctly."""
        serializer = self.user_serializer(self.user1)
        self.assertEqual(serializer.data['id'], self.user1.id)

    def test_email_field_content(self):
        """The serializer handles the instance.email field correctly."""
        serializer = self.user_serializer(self.user1)
        self.assertEqual(serializer.data['email'], self.user1.email)

    def test_username_field_content(self):
        """The serializer handles the instance.username field correctly."""
        serializer = self.user_serializer(self.user1)
        self.assertEqual(serializer.data['username'], self.user1.username)


class TestPostSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.post_serializer = serializers.PostSerializer
        cls.user_serializer = serializers.UserSerializer
        user1_data = td.create_user_data('mixin1')
        cls.user1 = models.User.objects.create(**user1_data)
        tag1_data = td.create_tag_data('mixin1')
        cls.tag1 = models.Tag.objects.create(**tag1_data)
        post1_data = td.create_post_data('mixin1', cls.user1)
        cls.post1 = models.Post.objects.create(**post1_data)
        cls.post1.tags.set([cls.tag1])

    def test_contains_expected_fields(self):
        """The serializer contains all the necessary fields."""
        serializer = self.post_serializer(self.post1)
        expected_fields = {
            'id',
            'title',
            'text',
            'created_at',
            'author',
            'tags',
            'is_public'
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_id_field_content(self):
        """The serializer handles the instance.title field correctly."""
        serializer = self.post_serializer(self.post1)
        self.assertEqual(serializer.data['id'], self.post1.id)

    def test_title_field_content(self):
        """The serializer handles the instance.title field correctly."""
        serializer = self.post_serializer(self.post1)
        self.assertEqual(serializer.data['title'], self.post1.title)

    def test_text_field_content(self):
        """The serializer handles the instance.text field correctly."""
        serializer = self.post_serializer(self.post1)
        self.assertEqual(serializer.data['text'], self.post1.text)

    def test_author_field_content(self):
        """The serializer handles the instance.author field correctly."""
        serializer = self.post_serializer(self.post1)
        expected_author = self.user_serializer(self.post1.author).data
        self.assertEqual(serializer.data['author'], expected_author)

    def test_created_at_field_content(self):
        """The serializer handles the instance.created_at field correctly."""
        serializer = self.post_serializer(self.post1)
        post_created_at = self.post1.created_at
        post_created_at_aware = post_created_at.astimezone(
            timezone.get_fixed_timezone(180)
        )
        expected_created_at = post_created_at_aware.isoformat()
        self.assertEqual(serializer.data['created_at'], expected_created_at)

    def test_tags_field_content(self):
        """The serializer handles the instance.tags field correctly."""
        serializer = self.post_serializer(self.post1)
        self.assertEqual(serializer.data['tags'], [self.tag1.id])

    def test_is_public_field_content(self):
        """The serializer handles the instance.is_public
        field correctly without report."""
        serializer = self.post_serializer(self.post1)
        self.assertEqual(serializer.data['is_public'], False)


class TestReportCreateSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.report_serializer = serializers.ReportCreateSerializer
        user1_data = td.create_user_data('mixin1')
        cls.user1 = models.User.objects.create(**user1_data)
        post1_data = td.create_post_data('mixin1', cls.user1)
        cls.post1 = models.Post.objects.create(**post1_data)
        report1_data = td.create_report_data(cls.post1)
        cls.report1 = models.Report.objects.create(**report1_data)

    def test_contains_expected_fields(self):
        """The serializer contains all the necessary fields."""
        serializer = self.report_serializer(self.report1)
        expected_fields = {
            'id',
            'post',
            'expire_time'
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_is_id_field_content(self):
        """The serializer handles the instance.id field correctly."""
        serializer = self.report_serializer(self.report1)
        self.assertEqual(serializer.data['id'], self.report1.id)

    def test_is_post_field_content(self):
        """The serializer handles the instance.post field correctly."""
        serializer = self.report_serializer(self.report1)
        self.assertEqual(serializer.data['post'], self.post1.id)

    def test_is_expire_time_field_content(self):
        """The serializer handles the instance.expire_time
        field correctly."""
        serializer = self.report_serializer(self.report1)
        report_expire_time = self.report1.expire_time
        post_created_at_aware = report_expire_time.astimezone(
            timezone.get_fixed_timezone(180)
        )
        expected_expire_time = post_created_at_aware.isoformat()
        self.assertEqual(serializer.data['expire_time'], expected_expire_time)
