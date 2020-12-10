from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.shortcuts import reverse
from django.utils import timezone

from .models import ShortURL


class ShortURLTest(TestCase):
    def test_creation(self):
        url = ShortURL.objects.create(url='http://google.com')

        self.assertIsNotNone(url.short_id)
        self.assertEqual(len(url.short_id), 7)

    def test_duplicate(self):
        url_base = ShortURL.objects.create(url='http://google.com')
        url = ShortURL.objects.create(
            url='http://google.com', short_id=url_base.short_id)

        self.assertNotEqual(url_base.short_id, url.short_id)

    def test_duplicate_deleted(self):
        url_base = ShortURL.objects.create(
            url='http://google.com', deleted_at=timezone.now())
        url = ShortURL.objects.create(
            url='http://google.com', short_id=url_base.short_id)

        self.assertNotEqual(url_base.short_id, url.short_id)


class ShortURLCleanupTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='123456')
        self.url_ok = ShortURL.objects.create(url='http://google.com')
        self.url_with_use = ShortURL.objects.create(
            url='http://google.com', accessed_at=timezone.now() - timedelta(days=31))
        self.url_user_without_use = ShortURL.objects.create(
            url='http://google.com', accessed_at=timezone.now() - timedelta(days=61), author=user, times_accessed=1)
        self.url_user_with_use = ShortURL.objects.create(
            url='http://google.com', accessed_at=timezone.now() - timedelta(days=61), author=user, times_accessed=10)

        call_command('clean_stale_urls')

    def test_expired_deleted(self):
        self.url_ok.refresh_from_db()
        self.url_with_use.refresh_from_db()
        self.url_user_without_use.refresh_from_db()

        self.assertIsNone(self.url_ok.deleted_at)
        self.assertIsNotNone(self.url_with_use.deleted_at)
        self.assertIsNotNone(self.url_user_without_use.deleted_at)
        self.assertIsNone(self.url_user_with_use.deleted_at)


class TestCreateUrlTest(TestCase):
    def test_anonymous_create(self):
        self.assertEqual(0, ShortURL.objects.count())

        response = self.client.post(
            '/api/urls/',
            {'url': 'http://google.com/'},
            content_type='application/json',
            HTTP_HOST='testserver',
        )
        data = response.data

        new_short_url = ShortURL.objects.get()
        self.assertEqual('http://google.com/', data['url'])
        self.assertEqual(
            f'http://testserver/r/?id={new_short_url.short_id}', data['alias'])
        self.assertIsNone(new_short_url.author)

    def test_create_with_author(self):
        user = User.objects.create_user(username='testuser', password='123456')
        self.client.login(username='testuser', password='123456')

        self.client.post(
            '/api/urls/',
            {'url': 'http://google.com/'},
            content_type='application/json',
            HTTP_HOST='testserver',
        )
        new_short_url = ShortURL.objects.get()
        self.assertEqual(user, new_short_url.author)
