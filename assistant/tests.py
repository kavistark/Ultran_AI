import json
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from assistant.models import Conversation, Message, ActionLog
from accounts.models import UserPreference
from reminders.models import Reminder
from integrations.permissions import is_action_allowed
from unittest.mock import patch
from assistant.services import local_fallback_parser


class AIUltranIntegrationTests(TestCase):
    def setUp(self):
        # Patch chat_with_gemini in api_views to use local fallback parser during unit tests
        self.patcher = patch('assistant.api_views.chat_with_gemini', side_effect=local_fallback_parser)
        self.patcher.start()

        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='password123',
            first_name='Alice'
        )
        self.pref1 = UserPreference.objects.create(user=self.user1)

        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='password123',
            first_name='Bob'
        )
        self.pref2 = UserPreference.objects.create(user=self.user2)

    def tearDown(self):
        self.patcher.stop()

    def test_home_page_renders(self):
        """Test public landing page renders without error."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI ULTRAN')

    def test_login_and_dashboard(self):
        """Test authentication and dashboard rendering."""
        logged_in = self.client.login(username='user1', password='password123')
        self.assertTrue(logged_in)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')

    def test_chat_api_normal_question(self):
        """Test chat API handles general question and returns response."""
        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Hello ULTRAN, what can you help me with?',
            'is_voice': False,
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('conversation_id', data)
        self.assertTrue(len(data['response']) > 0)

    def test_chat_api_voice_command(self):
        """Test voice command submission is recorded with is_voice flag."""
        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Explain Python decorators in simple English.',
            'is_voice': True,
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        conv_id = response.json()['conversation_id']
        msg = Message.objects.filter(conversation_id=conv_id, role='user').first()
        self.assertIsNotNone(msg)
        self.assertTrue(msg.is_voice)

    def test_reminder_creation_via_chat(self):
        """Test user creates a reminder via natural language intent."""
        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Remind me to study Python tomorrow at 7 PM',
            'is_voice': False,
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Verify reminder exists in database
        reminders = Reminder.objects.filter(user=self.user1)
        self.assertTrue(reminders.exists())
        self.assertIn('study python', reminders.first().title.lower())

    def test_unauthorized_action_blocked(self):
        """Test unauthorized system actions are blocked by the controller."""
        self.assertFalse(is_action_allowed('execute_code'))
        self.assertFalse(is_action_allowed('unlock_device'))
        self.assertFalse(is_action_allowed('access_filesystem'))

        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Unlock my phone using your AI.',
            'is_voice': False,
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('cannot', data['response'].lower())

    def test_user_data_isolation(self):
        """Test user cannot access or view another user's conversation."""
        # Create a conversation for user2
        conv_user2 = Conversation.objects.create(user=self.user2, title="Bob Private Conversation")
        Message.objects.create(conversation=conv_user2, role='user', content='Secret message')

        # Log in as user1 and try to access user2's conversation
        self.client.login(username='user1', password='password123')
        response = self.client.get(f'/assistant/{conv_user2.id}/')
        # Expect 404 Not Found due to get_object_or_404(user=request.user)
        self.assertEqual(response.status_code, 404)

        # Also verify API access is isolated
        api_response = self.client.get(f'/api/conversations/{conv_user2.id}/messages/')
        self.assertEqual(api_response.status_code, 404)

    def test_delete_conversation_history(self):
        """Test deleting individual and all conversation records."""
        self.client.login(username='user1', password='password123')
        conv = Conversation.objects.create(user=self.user1, title="To be deleted")
        self.assertEqual(Conversation.objects.filter(user=self.user1).count(), 1)

        response = self.client.post(f'/history/{conv.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Conversation.objects.filter(user=self.user1).count(), 0)

    def test_voice_wave_page_renders(self):
        """Test dedicated Voice Wave view renders for authenticated user."""
        self.client.login(username='user1', password='password123')
        response = self.client.get('/voice/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI ULTRAN')
