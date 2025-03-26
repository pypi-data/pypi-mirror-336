from django.conf import settings

from communication.configurations.communication import COMMUNICATION_TYPES

def get_all_communications_choices():
    allowed_communication_data = [
        (code, data['name'])
        for code, data in COMMUNICATION_TYPES.items()
    ]

    return allowed_communication_data

def get_allowed_communications_choices():
    allowed_communications = getattr(settings, 'ALLOWED_COMMUNICATION_TYPES', [])

    allowed_communication_data = [
        (str(code), COMMUNICATION_TYPES[code]['name'])
        for code in allowed_communications if code in COMMUNICATION_TYPES
    ]
    return allowed_communication_data


def get_allowed_communications(communication_event):
    allowed_communications = getattr(settings, 'ALLOWED_COMMUNICATION_TYPES', [])
    return allowed_communications