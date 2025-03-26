from communication.constants.communication_types import CommunicationTypes


COMMUNICATION_TYPES = {
    CommunicationTypes.EMAIL: {
        'name': 'EMAIL',
        'code': CommunicationTypes.EMAIL,
        'test_data_input_message': 'Enter the email',
        'recipients_key': 'emails',
        'data_key': 'email_data',
        'supported_providers': ['SMTP'],
        'provider_classes': {
            'SMTP': ('communication.services.email.smtp', 'SMTPEmailService'),
        },
        'config': {
            'provider': {
                'type': 'choice',
                'choices': ['SMTP'],
                'default': 'SMTP'
            },
            'smtp_host': {
                'type': 'string',
                'required': True,
                'depends_on': ['SMTP']
            },
            'smtp_port': {
                'type': 'integer',
                'required': True,
                'depends_on': ['SMTP']
            },
            'smtp_user': {
                'type': 'string',
                'required': True,
                'depends_on': ['SMTP']
            },
            'smtp_password': {
                'type': 'string',
                'required': True,
                'depends_on': ['SMTP']
            },
            'smtp_use_tls': {
                'type': 'string',
                'required': False,
                'depends_on': ['SMTP']
            },
        }
    },
    # CommunicationTypes.WHATSAPP: {
    #     'name': 'WhatsApp Messaging',
    #     'code': CommunicationTypes.WHATSAPP,
    #     'supported_providers': ['WHATSAPP_BUSINESS'],
    #     'config': {
    #         'provider': {
    #             'type': 'choice',
    #             'choices': ['WHATSAPP_BUSINESS'],
    #             'default': 'WHATSAPP_BUSINESS'
    #         },
    #         'whatsapp_from_number': {
    #             'type': 'string',
    #             'required': True,
    #             'depends_on': ['TWILIO', 'WHATSAPP_BUSINESS']
    #         },
    #         'whatsapp_business_api_url': {
    #             'type': 'string',
    #             'required': False,
    #             'depends_on': ['WHATSAPP_BUSINESS']
    #         },
    #     }
    # },
    # CommunicationTypes.PUSH_NOTIFICATIONS: {
    #     'name': 'PUSH NOTIFICATIONS',
    #     'code': CommunicationTypes.PUSH_NOTIFICATIONS,
    #     'supported_providers': ['FIREBASE', 'ONE_SIGNAL'],
    #     'config': {
    #         'provider': {
    #             'type': 'choice',
    #             'choices': ['FIREBASE', 'ONE_SIGNAL'],
    #             'default': 'FIREBASE'
    #         },
    #         'firebase_api_key': {
    #             'type': 'string',
    #             'required': True,
    #             'depends_on': ['FIREBASE']
    #         },
    #         'one_signal_app_id': {
    #             'type': 'string',
    #             'required': False,
    #             'depends_on': ['ONE_SIGNAL']
    #         },
    #         'one_signal_api_key': {
    #             'type': 'string',
    #             'required': False,
    #             'depends_on': ['ONE_SIGNAL']
    #         },
    #     }
    # }
}
