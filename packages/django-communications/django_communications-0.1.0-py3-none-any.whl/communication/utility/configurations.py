from django.conf import settings

from communication.configurations.communication import COMMUNICATION_TYPES


def validate_communication_config():
    try:
        for communication_type, config in settings.COMMUNICATION_CONFIG.items():
            # Retrieve the configuration definition for the communication type
            comm_type_config = COMMUNICATION_TYPES[communication_type]['config']

            # Get the provider chosen by the user
            provider = config.get('provider')

            if not provider:
                raise ValueError(f"Provider must be defined for {communication_type}.")

            # Ensure the provider is a valid choice from the configuration
            valid_providers = comm_type_config['provider']['choices']
            if provider not in valid_providers:
                raise ValueError(
                    f"Invalid provider '{provider}' selected for {communication_type}. Choose from {valid_providers}.")

            # Iterate through the configuration fields and check for required fields based on the selected provider
            for field, field_config in comm_type_config.items():
                # Skip the provider field itself
                if field == 'provider':
                    continue

                # Check if the field is required and if the provider matches the dependencies
                if field_config.get('required') and provider in field_config.get('depends_on', []):
                    if field not in config:
                        raise ValueError(
                            f"Missing required field '{field}' for provider '{provider}' in {communication_type}.")
        return True, "Configuration is valid!"
    except Exception as e:
        return False, str(e)
