import importlib
import json
import traceback

from django.conf import settings
from communication.configurations.communication import COMMUNICATION_TYPES
from communication.constants.communication_requests import CommunicationRequestsStatus
from communication.models import CommunicationEvents, CommunicationRequest
from communication.utility.communication_types import get_allowed_communications


class Communication:
    """
    Class to handle the initiation and management of communication requests.
    It validates the communication event, retrieves the necessary configurations, and processes communication requests.
    """

    def _validate_communication_event(self, communication_event_code):
        """
        Validates and fetches the CommunicationEvent object using the event code.

        :param communication_event_code: Unique identifier of the communication event.
        :return: CommunicationEvents object
        :raises: Exception if the event does not exist.
        """
        try:
            communication_event = CommunicationEvents.objects.get(code=communication_event_code)
            return communication_event
        except CommunicationEvents.DoesNotExist:
            raise ValueError(f"Communication event '{communication_event_code}' does not exist.")

    def initiate_communication(self, communication_event_code, data, *args, **kwargs):
        """
        Initiates communication for the specified event and data, processing each allowed communication type.

        :param communication_event_code: Code of the communication event.
        :param data: The data containing communication details such as recipients, content, etc.
        :param args: Additional arguments to be passed to provider's `send_communication` method.
        :param kwargs: Additional keyword arguments to be passed to provider's `send_communication` method.
        """
        try:
            # Validate and get the communication event object
            communication_event_obj = self._validate_communication_event(communication_event_code)

            # Get allowed communication types for the given event
            allowed_communications = get_allowed_communications(communication_event_obj)

            # Loop through each allowed communication type (e.g., email, push notifications)
            for communication_type in allowed_communications:
                # Retrieve the configuration for this communication type
                communication_config = COMMUNICATION_TYPES[communication_type]
                communication_setting_config = settings.COMMUNICATION_CONFIG.get(communication_type, {})

                # Get the necessary keys for the recipients and data from the configuration
                recipients_key = communication_config.get('recipients_key')
                communication_data_key = communication_config.get('data_key')

                # Extract the user and communication data from the provided data
                user = data.get('user')
                recipients = data.get(recipients_key, [])
                communication_data = data.get(communication_data_key, {})

                if not recipients or not communication_data:
                    continue

                # Get the selected provider class for the communication type
                selected_provider = communication_setting_config.get('provider')
                provider_class_path = communication_config.get('provider_classes', {}).get(selected_provider)
                if not provider_class_path:
                    raise ValueError(
                        f"Provider '{selected_provider}' not found for communication type '{communication_type}'.")

                # Dynamically import the provider class
                provider_class_path = communication_config['provider_classes'][selected_provider]
                module = importlib.import_module(*provider_class_path)
                class_name = provider_class_path[1]
                provider_class = getattr(module, class_name)

                # Instantiate the provider class
                provider_class_obj = provider_class(communication_config, communication_setting_config)

                # Iterate through each recipient and create a communication request for them
                for recipient in recipients:
                    communication_request = CommunicationRequest.objects.create(
                        communication_event=communication_event_obj,
                        data=json.dumps(communication_data),
                        recipients=[recipient],  # Store recipients as a list
                        user_id=user.id if user else None,
                        communication_type=communication_type
                    )

                    # Attempt to send the communication
                    try:
                        provider_class_obj.send_communication(recipient, communication_data, *args, **kwargs)

                        # Mark the request as successful and store the result
                        if isinstance(data, (dict, list, str, int, float, bool)):
                            communication_request.result = json.dumps(data)
                        else:
                            communication_request.result = ''
                        communication_request.status = CommunicationRequestsStatus.SUCCESS
                    except Exception as e:
                        # Capture and log the error traceback
                        communication_request.traceback = traceback.format_exc()

                        # request_object.next_attempt_time = datetime.now(timezone.utc) + timedelta(
                        #     minutes=COMMUNICATION_REQUESTS_RETRY_TIME_IN_MINUTES)

                        # Retry logic: Update status and increase retries count
                        communication_request.retries += 1
                        communication_request.status = CommunicationRequestsStatus.FAILED if communication_request.retries >= 3 else CommunicationRequestsStatus.RETRYING
                    finally:
                        # Save the communication request with updated status and result
                        communication_request.save()

        except Exception as e:
            # Raise an error if the whole process fails
            raise Exception(f"Error initiating communication: {str(e)}")
