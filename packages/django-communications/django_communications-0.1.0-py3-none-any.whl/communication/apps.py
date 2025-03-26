from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from communication.configurations.communication import COMMUNICATION_TYPES


class CommunicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communication'

    def ready(self):
        self.validate_communication_config()

    def validate_communication_config(self):
        # Step 1: Ensure COMMUNICATION_CONFIG is defined if ALLOWED_COMMUNICATION_TYPES is defined
        allowed_communications = getattr(settings, 'ALLOWED_COMMUNICATION_TYPES', [])

        communication_config_setting = getattr(settings, 'COMMUNICATION_CONFIG', [])
        if allowed_communications and not communication_config_setting:
            raise ImproperlyConfigured("COMMUNICATION_CONFIG is not defined in settings.")

        # Step 2: Validate COMMUNICATION_CONFIG for each allowed communication type
        for communication_type in allowed_communications:
            communication_type_name = COMMUNICATION_TYPES[communication_type]['name']

            # Step 2.1: Check if the communication type exists in COMMUNICATION_TYPES
            if communication_type not in COMMUNICATION_TYPES:
                raise ImproperlyConfigured(
                    f"'{communication_type}' is not valid communication type .")

            # Step 2.2: Get the communication config for the type
            base_communication_config = COMMUNICATION_TYPES[communication_type]
            communication_config = communication_config_setting[communication_type]

            # Step 2.3: Check if the provider is in supported_providers
            selected_provider = communication_config.get('provider')
            if not selected_provider:
                raise ImproperlyConfigured(
                    f"Provider for communication type '{communication_type_name}' is not provided.")
            if selected_provider not in base_communication_config['supported_providers']:
                raise ImproperlyConfigured(
                    f"Provider '{selected_provider}' for communication type '{communication_type_name}' is not supported.")

            # Step 2.4: Validate required fields based on provider
            for config_key, config_value in base_communication_config['config'].items():
                if 'depends_on' in config_value and config_value['required']:
                    depends_on_providers = config_value['depends_on']
                    if selected_provider not in depends_on_providers:
                        continue
                    if config_key not in communication_config:
                        raise ImproperlyConfigured(
                            f"Required configuration '{config_key}' for provider '{selected_provider}' is missing for communication type '{communication_type_name}'.")