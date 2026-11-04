import os
import re
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

DEFAULT_PHONE_NUMBER = "9092117397"


def format_e164_number(raw_number):
    """Normalize phone number to international E.164 format for cellular voice dialing."""
    if not raw_number:
        raw_number = DEFAULT_PHONE_NUMBER
    clean = re.sub(r'[^\d+]', '', str(raw_number).strip())
    if not clean:
        clean = DEFAULT_PHONE_NUMBER
    if clean.startswith('+'):
        return clean
    if len(clean) == 10:
        return f"+91{clean}"
    if clean.startswith('91') and len(clean) == 12:
        return f"+{clean}"
    return f"+{clean}"


def get_default_phone_number():
    """Retrieve the configured primary phone number for Kavi Stark."""
    env_phone = os.environ.get('USER_PHONE_NUMBER') or getattr(settings, 'USER_PHONE_NUMBER', None)
    return format_e164_number(env_phone or DEFAULT_PHONE_NUMBER)


def dispatch_reminder_call(reminder, user_name="Kavi Stark"):
    """
    Dispatch an automated outbound telephone call alert when a reminder or todo is due.
    1. If Twilio Cloud credentials are set (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER):
       Places an actual cellular telephone call via Twilio Voice API.
    2. Generates telemetry and direct click-to-dial `tel:` link for instant browser/mobile dialing.
    """
    raw_phone = reminder.phone_number or get_default_phone_number()
    target_phone = format_e164_number(raw_phone)
    reminder_title = reminder.title or "Scheduled Directive"

    telemetry = {
        'reminder_id': reminder.id,
        'title': reminder_title,
        'phone_number': target_phone,
        'method': 'web_call',
        'status': 'initiated',
        'call_url': f"tel:{target_phone}",
    }

    # 1. Twilio Outbound Voice Call Engine
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID') or getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN') or getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    twilio_from = os.environ.get('TWILIO_PHONE_NUMBER') or getattr(settings, 'TWILIO_PHONE_NUMBER', None)

    if account_sid and auth_token and twilio_from and not str(account_sid).startswith('your_'):
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)

            twiml_content = (
                f'<Response>'
                f'<Say voice="Polly.Matthew" rate="85%">'
                f'Attention, {user_name}. This is an urgent AI ULTRON voice directive. '
                f'Your scheduled reminder is due: {reminder_title}. '
                f'Repeating: {reminder_title}. Execute your directive without delay.'
                f'</Say>'
                f'</Response>'
            )

            call = client.calls.create(
                to=target_phone,
                from_=twilio_from,
                twiml=twiml_content
            )

            logger.info("Twilio cellular call placed to %s. Call SID: %s", target_phone, call.sid)
            telemetry['method'] = 'twilio'
            telemetry['call_sid'] = call.sid
            telemetry['status'] = 'dispatched'
            return telemetry
        except Exception as e:
            logger.warning("Twilio outbound voice call dispatch error: %s", str(e))
            telemetry['error'] = str(e)

    # 2. Local Telephony Dispatch Record (Direct Web Dialer / Softphone)
    logger.info("Automated reminder call alert queued for %s: '%s'", target_phone, reminder_title)
    return telemetry


def trigger_test_call(target_phone=None, user_name="Kavi Stark"):
    """Trigger an immediate test phone call to verify the telephony subsystem."""
    phone = format_e164_number(target_phone or get_default_phone_number())

    # Mock reminder object for testing
    class MockReminder:
        id = 9999
        title = "Ultron Telephony Diagnostic Verification"
        phone_number = phone

    return dispatch_reminder_call(MockReminder(), user_name=user_name)
