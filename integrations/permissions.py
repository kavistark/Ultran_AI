# Allowlist of permitted actions
ALLOWED_ACTIONS = {
    'create_reminder': {
        'description': 'Create a new reminder',
        'requires_confirmation': True,
        'required_fields': ['title', 'date', 'time'],
    },
    'list_reminders': {
        'description': 'List pending reminders',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'delete_reminder': {
        'description': 'Delete a reminder',
        'requires_confirmation': True,
        'required_fields': ['reminder_id'],
    },
    'create_task': {
        'description': 'Create a task',
        'requires_confirmation': False,
        'required_fields': ['title'],
    },
    'summarize_document': {
        'description': 'Summarize a document',
        'requires_confirmation': False,
        'required_fields': ['document_id'],
    },
    'open_link': {
        'description': 'Open an approved web link',
        'requires_confirmation': True,
        'required_fields': ['url'],
    },
    'general_chat': {
        'description': 'General conversation',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'capture_image': {
        'description': 'Capture and analyze camera frame',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'access_camera': {
        'description': 'Access camera stream for voice-requested visual inspection',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'system_diagnostics': {
        'description': 'Inspect host operational health, storage, and platform telemetry',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'calculate': {
        'description': 'Execute mathematical and quantitative calculations',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'search_knowledge': {
        'description': 'Retrieve knowledge domain synthesis',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'track_location': {
        'description': 'Retrieve geographic telemetry and location coordinates',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'get_location': {
        'description': 'Access location coordinates and geographical region',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'add_contact': {
        'description': 'Save new person and phone number to contact directory',
        'requires_confirmation': False,
        'required_fields': ['name', 'phone_number'],
    },
    'list_contacts': {
        'description': 'View contacts list in directory',
        'requires_confirmation': False,
        'required_fields': [],
    },
    'shutdown_system': {
        'description': 'Deactivate AI Ultron entity and close interface',
        'requires_confirmation': False,
        'required_fields': [],
    },
}

BLOCKED_ACTIONS = [
    'execute_code',
    'access_filesystem',
    'control_hardware',
    'unlock_device',
    'send_message_as_user',
    'access_private_accounts',
]


def is_action_allowed(action_type):
    return action_type in ALLOWED_ACTIONS and action_type not in BLOCKED_ACTIONS


def get_action_config(action_type):
    return ALLOWED_ACTIONS.get(action_type, {})
