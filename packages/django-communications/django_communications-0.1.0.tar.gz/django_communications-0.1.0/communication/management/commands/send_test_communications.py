import importlib

from django.conf import settings
from django.core.management.base import BaseCommand

from communication.configurations.communication import COMMUNICATION_TYPES


class Command(BaseCommand):
    help = 'Send test communications to the recipients of allowed communication types'

    def handle(self, *args, **kwargs):
        # Step 1: Get all the allowed communication types
        allowed_communications = getattr(settings, 'ALLOWED_COMMUNICATION_TYPES', [])
        if not allowed_communications:
            self.stdout.write(self.style.WARNING("No allowed communication types found."))
            return

        communication_config_settings = settings.COMMUNICATION_CONFIG

        # Step 2: Get recipients for each allowed communication type
        for communication_type in allowed_communications:
            communication_config = COMMUNICATION_TYPES[communication_type]

            self.stdout.write(self.style.HTTP_INFO(f"Processing communication type: {communication_config['name']}"))

            # Check if communication type exists in config
            if communication_type not in COMMUNICATION_TYPES:
                self.stdout.write(self.style.WARNING(f"Warning: Communication type '{communication_config['name']}' not found in COMMUNICATION_TYPES."))
                continue

            communication_setting_config = communication_config_settings.get(communication_type, {})

            recipient = input(f"{communication_config['test_data_input_message']} ")

            selected_provider = communication_setting_config.get('provider')
            provider_class_path = communication_config.get('provider_classes', {}).get(selected_provider)

            if not provider_class_path:
                self.stdout.write(self.style.ERROR(f"Error: Provider '{selected_provider}' not found for communication type '{communication_config['name']}'."))
                continue

            # Dynamically import the provider class
            try:
                module = importlib.import_module(*provider_class_path)
                class_name = provider_class_path[1]
                provider_class = getattr(module, class_name)
            except (ImportError, AttributeError) as e:
                self.stdout.write(self.style.ERROR(f"Error importing provider class '{provider_class_path}': {e}"))
                continue

            # Instantiate the provider class
            try:
                provider_class_obj = provider_class(communication_config, communication_setting_config)
                provider_class_obj.send_test_communication(recipient)
                self.stdout.write(self.style.SUCCESS(f"Test communication sent to {recipient} for {communication_config['name']}."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error sending test communication for {communication_config['name']}: {e}"))
