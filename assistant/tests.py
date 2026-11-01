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


class AIUltronIntegrationTests(TestCase):
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
        self.assertContains(response, 'AI ULTRON')

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
            'message': 'Hello ULTRON, what can you help me with?',
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
        self.assertContains(response, 'AI ULTRON')

    def test_camera_vision_analysis(self):
        """Test voice camera capture and image analysis."""
        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Take a picture and tell me what you see',
            'is_voice': True,
            'image_data': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA=',
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertTrue(len(data['response']) > 0)
        self.assertNotIn('resolution', data['response'].lower())
        self.assertNotIn('pixel', data['response'].lower())
        self.assertNotIn('dimension', data['response'].lower())

    def test_location_tracking(self):
        """Test voice location tracking intent and coordinates."""
        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Track my location and report coordinates',
            'is_voice': True,
            'location_data': {'latitude': 13.0827, 'longitude': 80.2707, 'timezone': 'Asia/Kolkata'},
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('location', data['response'].lower())
        self.assertEqual(data.get('tool_executed'), 'track_location')

    def test_calling_system_decommissioned(self):
        """Test that calling directives confirm telephony and calling subsystems are decommissioned."""
        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Ultron, calling process Sarah',
            'is_voice': True,
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('decommissioned', data['response'].lower())

    def test_contact_management_directives(self):
        """Test adding and listing contacts via voice/chat."""
        from assistant.models import Contact
        self.client.login(username='user1', password='password123')

        # Add contact
        add_res = self.client.post(
            '/api/chat/',
            data=json.dumps({'message': 'Add contact Tony 9123456780', 'is_voice': True}),
            content_type='application/json'
        )
        self.assertEqual(add_res.status_code, 200)
        self.assertTrue(Contact.objects.filter(user=self.user1, name='Tony').exists())

        # List contacts
        list_res = self.client.post(
            '/api/chat/',
            data=json.dumps({'message': 'List contacts', 'is_voice': True}),
            content_type='application/json'
        )
        self.assertEqual(list_res.status_code, 200)
        self.assertIn('Tony', list_res.json()['response'])

    def test_shutdown_directive(self):
        """Test shutdown command deactivates system."""
        self.client.login(username='user1', password='password123')
        res = self.client.post(
            '/api/chat/',
            data=json.dumps({'message': 'Ultron, shut down', 'is_voice': True}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['action']['intent'], 'shutdown_system')
        self.assertIn('shutting down', data['response'].lower())

    def test_phone_number_inquiries(self):
        """Test Ultron clarifies telephony is decommissioned when queried for phone number."""
        self.client.login(username='user1', password='password123')
        # What is your number
        res1 = self.client.post(
            '/api/chat/',
            data=json.dumps({'message': 'What is your number?'}),
            content_type='application/json'
        )
        self.assertEqual(res1.status_code, 200)
        self.assertIn('decommissioned', res1.json()['response'].lower())

    def test_reminder_creates_call_on_due(self):
        """Test creating reminder binds call_on_due=True."""
        self.client.login(username='user1', password='password123')
        payload = {
            'message': 'Remind me to review deployment tomorrow at 10 AM',
            'is_voice': True,
        }
        response = self.client.post(
            '/api/chat/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        rem = Reminder.objects.filter(user=self.user1, title__icontains='review deployment').first()
        self.assertIsNotNone(rem)
        self.assertTrue(rem.call_on_due)
        self.assertFalse(rem.called)

    def test_due_reminders_trigger_call(self):
        """Test due reminders API marks reminders as called and returns phone telemetry."""
        # Create a past due reminder
        past_time = timezone.now() - timedelta(minutes=5)
        rem = Reminder.objects.create(
            user=self.user1,
            title='Critical Reactor Core Check',
            due_time=past_time,
            call_on_due=True,
            phone_number='9092117397',
            called=False,
            status='pending',
        )
        self.client.login(username='user1', password='password123')
        response = self.client.get('/api/reminders/due/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('due_reminders', data)
        self.assertTrue(any(r['id'] == rem.id for r in data['due_reminders']))
        
        # Verify database record updated
        rem.refresh_from_db()
        self.assertTrue(rem.called)
        self.assertEqual(rem.status, 'completed')

    def test_initiate_call_api_endpoint_removed(self):
        """Test direct /api/call/ endpoint has been removed (returns 404)."""
        response = self.client.post(
            '/api/call/',
            data=json.dumps({'to': '9092117397'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_tts_api_post(self):
        """Test Deep Cinematic Voice TTS API endpoint with POST."""
        self.client.login(username='user1', password='password123')
        payload = {'text': 'I am AI ULTRON. State your directive, Kavi Stark.'}
        response = self.client.post(
            '/api/tts/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(response['Content-Type'], ['audio/mpeg', 'audio/wav'])
        self.assertTrue(len(response.content) > 100)

    def test_tts_api_get(self):
        """Test Deep Cinematic Voice TTS API endpoint with GET query."""
        response = self.client.get('/api/tts/?text=State+your+directive')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response['Content-Type'], ['audio/mpeg', 'audio/wav'])
        self.assertTrue(len(response.content) > 100)

    def test_tts_api_empty_text(self):
        """Test Deep Cinematic Voice TTS API returns 400 for empty text."""
        response = self.client.post(
            '/api/tts/',
            data=json.dumps({'text': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_boss_identity_kavi_stark(self):
        """Test that AI ULTRON recognizes Kavi Stark as boss."""
        self.client.login(username='user1', password='password123')
        response = self.client.post(
            '/api/chat/',
            data=json.dumps({'message': 'Who is your boss?'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('Kavi Stark', data['response'])

    def test_human_perception_and_identity(self):
        """Test human behavioral queries: who am i, can you hear me, who are you."""
        self.client.login(username='user1', password='password123')
        for q, expected in [
            ('who am i', 'Kavi Stark'),
            ('can you hear me', 'acoustic perception'),
            ('who are you', 'AI ULTRON'),
        ]:
            resp = self.client.post('/api/chat/', data=json.dumps({'message': q}), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(expected.lower(), resp.json()['response'].lower())

    def test_filler_words_and_math(self):
        """Test that human speech filler words are stripped and math expressions evaluated."""
        self.client.login(username='user1', password='password123')
        resp = self.client.post(
            '/api/chat/',
            data=json.dumps({'message': 'uhm like what is 50 times 4'}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('200', resp.json()['response'])

    def test_gemini_key_config_api(self):
        """Test GET and POST on /api/config/gemini-key/."""
        resp = self.client.get('/api/config/gemini-key/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['model'], 'gemini-2.0-flash')

    def test_voice_wave_alias_url(self):
        """Test that /voice-wave/ alias renders correctly without 404."""
        resp = self.client.get('/voice-wave/')
        self.assertEqual(resp.status_code, 200)

