from datetime import timedelta
from pprint import pprint

from django.shortcuts import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api import serializers
from posts import models


def create_user_data(type):
    """Retrieves the data type, and based on it
    returns the data necessary to create a user."""
    user_data = {
        'username': f'Username{type}',
        'password': f'password{type}'
    }
    return user_data


def create_post_data(type, author):
    """Retrieves the data type, and based on it
    returns the data necessary to create a post."""
    post_data = {
        'title': f'Title of {type} post',
        'text': f'Text of {type} post',
        'created_at': timezone.now(),
        'author': author
    }
    return post_data


def create_report_data(post, expire_after):
    report_data = {
        'post': post,
        'expire_time': timezone.now() + expire_after
    }
    return report_data


def create_tag_data(type):
    """Retrieves the data type, and based on it
    returns the data necessary to create a tag."""
    tag_data = {
        'name': f'Name of {type} tag',
        'description': f'Description of {type} tag'
    }
    return tag_data


class PostsApiTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user1_data = create_user_data('mixin1')
        cls.user1 = models.User.objects.create(**user1_data)
        tag1_data = create_tag_data('mixin1')
        cls.tag1 = models.Tag.objects.create(**tag1_data)
        post1_data = create_post_data('mixin1', cls.user1,)
        cls.post1 = models.Post.objects.create(**post1_data)
        cls.post1.tags.set([cls.tag1])

    def setUp(self):
        self.guest_client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user1)

    def test_get_list_posts(self):
        """Authenticated user can get list of posts."""
        url = reverse('api:post-list')
        response = self.auth_client.get(url)
        serializer = serializers.PostSerializer([self.post1], many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_post(self):
        """Authenticated user can create a posts."""
        url = reverse('api:post-list')
        post_data = create_post_data('test1', self.user1)
        post_data.update({'tags': [self.tag1.id]})
        posts_cnt = models.Post.objects.count()
        response = self.auth_client.post(url, data=post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Post.objects.count(), posts_cnt + 1)

    def test_user_can_patch_post(self):
        """Authenticated user can patch the posts."""
        #  first, we will create a post so that we can change it later
        post_data = create_post_data('test1', self.user1)
        post = models.Post.objects.create(**post_data)
        changed_title = 'Changed title'
        post_data['title'] = changed_title
        url = reverse('api:post-detail', args=(post.id,))
        response = self.auth_client.patch(url, data=post_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            models.Post.objects.get(id=post.id).title,
            changed_title
        )

    def test_user_can_delete_post(self):
        """Authenticated user can delete the posts."""
        #  first, we will create a post to delete it after
        post_data = create_post_data('test1', self.user1)
        post = models.Post.objects.create(**post_data)
        posts_cnt = models.Post.objects.count()
        url = reverse('api:post-detail', args=(post.id,))
        response = self.auth_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Post.objects.count(), posts_cnt - 1)


class PostsApiTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user1_data = create_user_data('mixin1')
        cls.user1 = models.User.objects.create(**user1_data)
        tag1_data = create_tag_data('mixin1')
        cls.tag1 = models.Tag.objects.create(**tag1_data)
        post1_data = create_post_data('mixin1', cls.user1,)
        cls.post1 = models.Post.objects.create(**post1_data)
        cls.post1.tags.set([cls.tag1])
        report1_data = create_report_data(cls.post1, timedelta(days=1))
        cls.report1 = models.Report.objects.create(**report1_data)

    def setUp(self):
        self.guest_client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user1)

    def test_get_list_reports(self):
        """Authenticated user can get list of reports."""
        url = reverse('api:report-list')
        response = self.auth_client.get(url)
        serializer = serializers.ReportViewSerializer(
            [self.report1],
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_post(self):
        """Authenticated user can create a posts."""
        url = reverse('api:report-list')
        data = create_report_data(self.post1.id, timedelta(days=1))
        report_cnt = models.Report.objects.count()
        response = self.auth_client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Report.objects.count(), report_cnt + 1)
