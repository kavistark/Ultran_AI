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
}

BLOCKED_ACTIONS = [
    'execute_code',
    'access_filesystem',
    'control_hardware',
    'access_camera',
    'unlock_device',
    'send_message_as_user',
    'access_private_accounts',
]


def is_action_allowed(action_type):
    return action_type in ALLOWED_ACTIONS and action_type not in BLOCKED_ACTIONS


def get_action_config(action_type):
    return ALLOWED_ACTIONS.get(action_type, {})
