from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.mail.message import EmailMessage

class SMTPEmailService:
    def __init__(self, communication_config, communication_setting_config):
        # Assign SMTP settings dynamically
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        settings.EMAIL_HOST = communication_setting_config['smtp_host']
        settings.EMAIL_PORT = communication_setting_config['smtp_port']
        settings.EMAIL_HOST_USER = communication_setting_config['smtp_user']
        settings.EMAIL_HOST_PASSWORD = communication_setting_config['smtp_password']

        smtp_use_tls = communication_setting_config.get('smtp_use_tls')
        if smtp_use_tls is not None:
            settings.EMAIL_USE_TLS = smtp_use_tls

    def send_communication(self, recipient, data):
        """Send the email based on the communication data."""

        subject = data.get('subject')
        content = data.get('content')
        attachments = data.get('attachments', [])

        if not recipient:
            raise ValidationError("No Email Provided")

        # Create the email message
        email_message = EmailMessage(
            subject=subject,
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient],
        )

        # Attach any files if provided
        for attachment in attachments:
            email_message.attach(attachment['name'], attachment['content'], attachment['content_type'])

        email_message.send()

    def send_test_communication(self, recipient):
        """Send a test email to verify the configuration and email sending process."""

        # Prepare test content and subject
        subject = "Test Email - SMTP Configuration"
        content = "This is a test email to verify the SMTP email configuration."

        # Send the test email
        self.send_communication(recipient, {
            'subject': subject,
            'content': content
        })
