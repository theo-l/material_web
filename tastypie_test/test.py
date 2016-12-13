# encoding: utf-8
import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCase
from .models import Entry


class EntryResourceTest(ResourceTestCase, TestCase):

    fixtures = [test_entries.json]
    api_pattern = '/api/v1/{}/'

    def setUp(self):
        super(EntryResourceTest, self).setUp()
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(
            self.username, 'daniel@example.com', self.password)

        self.entry_1 = Entry.objects.get(slug='first-post')
        self.detail_url = '/api/v1/entry/{0}/'.format(self.entry_1.pk)

        self.post_data = {
            'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'Second Post',
            'slug': 'second-post',
            'created': '2012-05-01T22:05:12'

        }

    def get_credentials(self):
        return self.create_basic(
            username=self.username, password=self.password
        )

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(
            self.api_client.get(
                self.api_pattern.format('entry'), format='json'
            )
        )
