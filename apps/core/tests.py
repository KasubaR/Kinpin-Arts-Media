from unittest.mock import patch

from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.core.models import NewsletterSubscriber
from apps.core.services.mailchimp import MailchimpSyncResult


class NewsletterSubscribeViewTests(TestCase):
    def _post_newsletter(self, email='test@example.com'):
        return self.client.post(
            reverse('newsletter_subscribe'),
            {'email': email},
            HTTP_REFERER=reverse('home'),
            follow=True,
        )

    @override_settings(
        MAILCHIMP_ENABLED=True,
        MAILCHIMP_API_KEY='test-key',
        MAILCHIMP_AUDIENCE_ID='audience-id',
        MAILCHIMP_SERVER_PREFIX='us1',
        MAILCHIMP_DOUBLE_OPTIN=True,
    )
    @patch('apps.core.views.subscribe_email')
    def test_newsletter_subscribe_success_sync(self, mock_subscribe_email):
        mock_subscribe_email.return_value = MailchimpSyncResult(success=True, status='synced')

        response = self._post_newsletter()

        self.assertEqual(response.status_code, 200)
        subscriber = NewsletterSubscriber.objects.get(email='test@example.com')
        self.assertEqual(subscriber.sync_status, NewsletterSubscriber.SYNC_SYNCED)
        self.assertIsNotNone(subscriber.sync_last_attempt_at)
        self.assertEqual(subscriber.sync_error_message, '')

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You are subscribed. Please check your inbox to confirm.', messages)

    @override_settings(
        MAILCHIMP_ENABLED=True,
        MAILCHIMP_API_KEY='test-key',
        MAILCHIMP_AUDIENCE_ID='audience-id',
        MAILCHIMP_SERVER_PREFIX='us1',
        MAILCHIMP_DOUBLE_OPTIN=True,
    )
    @patch('apps.core.views.subscribe_email')
    def test_existing_subscriber_remains_idempotent(self, mock_subscribe_email):
        NewsletterSubscriber.objects.create(email='test@example.com')
        mock_subscribe_email.return_value = MailchimpSyncResult(success=True, status='already_synced')

        response = self._post_newsletter()

        self.assertEqual(NewsletterSubscriber.objects.filter(email='test@example.com').count(), 1)
        subscriber = NewsletterSubscriber.objects.get(email='test@example.com')
        self.assertEqual(subscriber.sync_status, NewsletterSubscriber.SYNC_ALREADY_SYNCED)
        self.assertIsNotNone(subscriber.sync_last_attempt_at)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You are already subscribed.', messages)

    @override_settings(
        MAILCHIMP_ENABLED=True,
        MAILCHIMP_API_KEY='test-key',
        MAILCHIMP_AUDIENCE_ID='audience-id',
        MAILCHIMP_SERVER_PREFIX='us1',
        MAILCHIMP_DOUBLE_OPTIN=True,
    )
    @patch('apps.core.views.subscribe_email')
    def test_contact_limit_keeps_local_subscriber(self, mock_subscribe_email):
        mock_subscribe_email.return_value = MailchimpSyncResult(
            success=False,
            status='contact_limit',
            message='Free plan contact limit reached.',
        )

        response = self._post_newsletter()

        subscriber = NewsletterSubscriber.objects.get(email='test@example.com')
        self.assertEqual(subscriber.sync_status, NewsletterSubscriber.SYNC_CONTACT_LIMIT)
        self.assertEqual(subscriber.sync_error_message, 'Free plan contact limit reached.')
        self.assertLessEqual(subscriber.sync_last_attempt_at, timezone.now())

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            'Thanks. You are saved on our waitlist while we clear mailing list capacity.',
            messages,
        )

    @override_settings(MAILCHIMP_ENABLED=False)
    @patch('apps.core.views.subscribe_email')
    def test_mailchimp_disabled_uses_local_only_flow(self, mock_subscribe_email):
        response = self._post_newsletter()

        subscriber = NewsletterSubscriber.objects.get(email='test@example.com')
        self.assertEqual(subscriber.sync_status, NewsletterSubscriber.SYNC_PENDING)
        self.assertIsNone(subscriber.sync_last_attempt_at)
        self.assertEqual(subscriber.sync_error_message, '')
        mock_subscribe_email.assert_not_called()

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('You are subscribed. Please check your inbox to confirm.', messages)
