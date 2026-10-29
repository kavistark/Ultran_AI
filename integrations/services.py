from .permissions import is_action_allowed, get_action_config


def validate_action(action_dict):
    """
    Validate a structured action from Gemini.
    Returns (is_valid, reason).
    """
    action_type = action_dict.get('intent', '')

    if not is_action_allowed(action_type):
        return False, f"Action '{action_type}' is not permitted by the system."

    config = get_action_config(action_type)
    for field in config.get('required_fields', []):
        if not action_dict.get(field):
            return False, f"Missing required field: {field}"

    return True, "Action is valid."
