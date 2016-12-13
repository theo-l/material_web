# encoding: utf-8
import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCase
from .models import Entry

api_pattern = '/api/v1/'
entry_list_pattern = api_pattern + 'entries/'
entry_detail_pattern = '/api/v1/entry/{0}/'
user_detail_pattern = api_pattern + 'user/{0}/'


class EntryResourceTest(ResourceTestCase, TestCase):

    fixtures = [test_entries.json]

    def setUp(self):
        super(EntryResourceTest, self).setUp()
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(
            self.username, 'daniel@example.com', self.password)

        self.entry_1 = Entry.objects.get(slug='first-post')
        self.detail_url = entry_detail_pattern.format(self.entry_1.pk)

        self.post_data = {
            'user': user_detail_pattern.format(self.user.pk),
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
                entry_list_pattern, format='json'
            )
        )

    def test_get_list_json(self):
        resp = self.api_client.get(
            entry_list_pattern,
            format='json', authentication=self.get_credentials()
        )
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)['objects']), 12)
        self.assertEqual(self.deserialize(resp)['objects'][0],
                         {
            'pk': str(self.entry_1.pk),
            'user': user_detail_pattern.format(self.user.pk),
            'title': 'First post',
            'slug': 'first-post',
            'created': '2012-05-01T19:13:42',
            'resource_url': entry_detail_pattern.format(self.entry_1.pk)
        }
        )

    def test_get_list_xml(self):
        self.assertValidXMLResponse(
            self.api_client.get(entry_list_pattern, format='json')
        )

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(
            self.api_client.get(self.detail_url, format='json'))

    def test_get_detail_json(self):
        resp = self.api_client.get(
            self.detail_url, format='json',
            authentication=self.get_credentials()
        )
        self.assertValidJSONResponse(resp)

        self.assertKeys(
            self.deserialize(resp), ['created', 'slug', 'title', 'user'])
        self.assertEqual(self.deserialize(resp)['name'], 'First Post')

    def test_get_detail_xml(self):
        self.assertValidXMLResponse(self.api_client.get(
            self.detail_url, format='json', authentication=self.get_credentials()))

        def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(
            self.api_client.put(self.detail_url, format='json', data={}))

    def test_put_detail(self):
        # Grab the current data & modify it slightly.
        original_data = self.deserialize(self.api_client.get(
            self.detail_url, format='json', authentication=self.get_credentials()))
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Post'
        new_data['created'] = '2012-05-01T20:06:12'

        self.assertEqual(Entry.objects.count(), 5)
        self.assertHttpAccepted(self.api_client.put(
            self.detail_url, format='json', data=new_data, authentication=self.get_credentials()))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(Entry.objects.count(), 5)
        # Check for updated data.
        self.assertEqual(Entry.objects.get(pk=25).title, 'Updated: First Post')
        self.assertEqual(Entry.objects.get(pk=25).slug, 'first-post')
        self.assertEqual(
            Entry.objects.get(pk=25).created, datetime.datetime(2012, 3, 1, 13, 6, 12))

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(
            self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.assertEqual(Entry.objects.count(), 5)
        self.assertHttpAccepted(self.api_client.delete(
            self.detail_url, format='json', authentication=self.get_credentials()))
        self.assertEqual(Entry.objects.count(), 4)
