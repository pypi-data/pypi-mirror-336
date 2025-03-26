# django-communications

## Overview
`django-communications` is a Django package designed to provide a central platform for sending different types of communications such as emails, SMS, WhatsApp messages, push notifications, and more. Currently, it supports sending emails using an SMTP provider.

## Installation
To install `django-communications`, use pip:
```sh
pip install django-communications
```

## Configuration
Add `communication` to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'communication',
]
```

### Settings
Define the allowed communication types and configuration settings in `settings.py`:
```python
from communication.constants.communication_types import CommunicationTypes
from communication.constants.providers import EmailProviders

ALLOWED_COMMUNICATION_TYPES = [CommunicationTypes.EMAIL]

COMMUNICATION_CONFIG = {
    CommunicationTypes.EMAIL: {
        'provider': EmailProviders.SMTP,
        'smtp_host': 'smtp.gmail.com',
        'smtp_port': '587',
        'smtp_user': '',
        'smtp_password': '',
        'smtp_use_tls': True
    }
}
```

## Creating a Communication Event
Before sending communications, you need to create a **Communication Event**. This can be done through the Django Admin panel:
1. Navigate to **Communication Events** in the Django Admin.
2. Click **Add Communication Event**.
3. Define a **Code** for the event.
4. Select the allowed **Communication Types**.
5. Ignore the fields **Default Value** and **Can User Change Preference** (reserved for future use).
6. Save the event.

Once created, save the event's code in your constants for future use.

## Sending a Communication
To send a communication, create a `data_dict` with the necessary details:

```python
data_dict = {
    'emails': ['example@example.com'],
    'email_data': {
        'subject': "This is a Subject",
        'content': "This is content",  # Content can be plain text or HTML
        'attachments': []  # List of file paths if needed
    }
}
```

Then, initiate the communication using:
```python
from communication.communication import Communication

Communication().initiate_communication("{communication_event_code}", data_dict)
```

### Background Processing
You can also send communications in the background using Celery or threads to improve performance:
```python
from threading import Thread
Thread(target=Communication().initiate_communication, args=("{communication_event_code}", data_dict)).start()
```

## Viewing Logs
All sent communications can be viewed in the Django Admin under **Communication Requests**, allowing tracking and debugging.

## Future Enhancements
- Support for additional communication channels (SMS, WhatsApp, Push Notifications, etc.).
- User preference management for different communication types.

## Contributing
If you'd like to contribute to `django-communications`, feel free to submit a pull request or report issues on the GitHub repository.

## License
`django-communications` is open-source and available under the MIT License.

