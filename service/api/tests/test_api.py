from datetime import timedelta

from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient

from api import serializers
from api.tests import test_data as td
from posts import models


class PostsApiTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user1_data = td.create_user_data('mixin1')
        cls.user1 = models.User.objects.create(**user1_data)
        post1_data = td.create_post_data('mixin1', cls.user1)
        cls.post1 = models.Post.objects.create(**post1_data)
        tag1_data = td.create_tag_data('mixin1')
        cls.tag1 = models.Tag.objects.create(**tag1_data)
        cls.post1.tags.set([cls.tag1])

    def setUp(self):
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(self.user1)

    def test_get_list_posts(self):
        """Authenticated user can get list of posts."""
        url = reverse('api:post-list')
        response = self.auth_client.get(url)
        context = {'request': APIRequestFactory().get('/')}
        serializer = serializers.PostViewSerializer(
            [self.post1],
            many=True,
            context=context
        )
        is_public = response.data[0].pop('is_public')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(is_public, False)

    def test_user_can_create_post(self):
        """Authenticated user can create a posts."""
        posts_cnt = models.Post.objects.count()
        url = reverse('api:post-list')
        post_data = td.create_post_data('test1', self.user1)
        post_data.update({'tags': [self.tag1.id]})
        response = self.auth_client.post(url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Post.objects.count(), posts_cnt + 1)

    def test_user_can_patch_post(self):
        """Authenticated user can patch the posts."""
        post_data = td.create_post_data('test1', self.user1)
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
        post_data = td.create_post_data('test1', self.user1)
        post = models.Post.objects.create(**post_data)
        posts_cnt = models.Post.objects.count()
        url = reverse('api:post-detail', args=(post.id,))
        response = self.auth_client.delete(url)
        new_response = self.auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Post.objects.count(), posts_cnt - 1)
        self.assertEqual(new_response.status_code, status.HTTP_404_NOT_FOUND)


class ReportApiTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user1_data = td.create_user_data('mixin1')
        cls.user1 = models.User.objects.create(**user1_data)
        tag1_data = td.create_tag_data('mixin1')
        cls.tag1 = models.Tag.objects.create(**tag1_data)
        post1_data = td.create_post_data('mixin1', cls.user1,)
        cls.post1 = models.Post.objects.create(**post1_data)
        cls.post1.tags.set([cls.tag1])
        report1_data = td.create_report_data(cls.post1)
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

    def test_create_report(self):
        """Authenticated user can create a posts."""
        url = reverse('api:report-list')
        data = td.create_report_data(self.post1.id)
        report_cnt = models.Report.objects.count()
        response = self.auth_client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Report.objects.count(), report_cnt + 1)

    def test_user_can_patch_report(self):
        """Authenticated user can patch a posts."""
        report_data = td.create_report_data(self.post1)
        report = models.Report.objects.create(**report_data)
        another_post_data = td.create_post_data('test', report.post.author)
        another_post = models.Post.objects.create(**another_post_data)
        patch_data = {'post': another_post.id}
        url = reverse('api:report-detail', args=(report.id,))
        response = self.auth_client.patch(url, data=patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['post'], another_post.id)

    def test_user_can_delete_report(self):
        """Authenticated user can patch a report."""
        report_data = td.create_report_data(self.post1)
        report = models.Report.objects.create(**report_data)
        reports_cnt = models.Report.objects.count()
        url = reverse('api:report-detail', args=(report.id,))
        response = self.auth_client.delete(url)
        new_response = self.auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Report.objects.count(), reports_cnt - 1)
        self.assertEqual(new_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_create_report_with_invalid_post(self):
        """Tests that the user cannot create an ad with someone else's post"""
        test_user_data = td.create_user_data('test')
        test_user = models.User.objects.create(**test_user_data)
        another_post_data = td.create_post_data('test', test_user)
        another_post = models.Post.objects.create(**another_post_data)
        reports_cnt = models.Report.objects.count()
        url = reverse('api:report-list')
        request_data = td.create_report_data(another_post.id)
        response = self.auth_client.post(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Report.objects.count(), reports_cnt)

    def test_user_cant_create_report_with_expire_time_lt_now(self):
        """The user cannot create a report where the
        expiration time is less than now."""
        test_report_data = td.create_report_data(self.post1.id)
        test_report_data['expire_time'] -= timedelta(days=2)
        reports_cnt = models.Report.objects.count()
        url = reverse('api:report-list')
        response = self.auth_client.post(url, test_report_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Report.objects.count(), reports_cnt)
