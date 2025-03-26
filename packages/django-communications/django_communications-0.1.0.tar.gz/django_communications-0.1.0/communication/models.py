import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from communication.configurations.communication import COMMUNICATION_TYPES
from communication.constants.communication_requests import CommunicationRequestsStatus
from communication.constants.communication_types import CommunicationTypes
from communication.utility.communication_types import get_allowed_communications_choices, get_all_communications_choices

User = get_user_model()

class CommunicationEvents(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'communication_events'
        verbose_name = 'Communication Event'
        verbose_name_plural = 'Communication Events'
        ordering = ['name']


class CommunicationEventsConfigurations(models.Model):
    communication_event = models.ForeignKey(CommunicationEvents, on_delete=models.CASCADE,
                                            related_name='configurations')
    communication_type = models.CharField(
        max_length=50,
        choices=get_allowed_communications_choices(),
    )
    allowed = models.BooleanField(default=True)
    default_value = models.BooleanField(default=False)
    can_user_change_preference = models.BooleanField(default=True)

    def __str__(self):
        return f"{str(self.communication_event)} - {COMMUNICATION_TYPES[self.communication_type]['name']}"

    class Meta:
        db_table = 'communication_events_configurations'
        verbose_name = 'Communication Event Configuration'
        verbose_name_plural = 'Communication Event Configurations'
        unique_together = ['communication_event', 'communication_type']


# class UserPreferences(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="preferences")
#     communication_event = models.ForeignKey(CommunicationEvents, on_delete=models.CASCADE,
#                                             related_name="user_preferences")
#     communication_event_configuration = models.ForeignKey(CommunicationEventsConfigurations, on_delete=models.CASCADE,
#                                             related_name="configuration_user_preferences")
#
#     allowed = models.BooleanField(default=True)
#
#     def __str__(self):
#         return f"{str(self.user)} - {str(self.communication_event)}"
#
#     class Meta:
#         db_table = 'user_preferences'
#         verbose_name = _('User Preference')
#         verbose_name_plural = _('User Preferences')
#         unique_together = ['user', 'communication_event', 'communication_event_configuration']
#         indexes = [
#             models.Index(fields=['user', 'communication_event']),
#         ]



class CommunicationRequest(models.Model):
    status_choices = (
        (CommunicationRequestsStatus.PENDING, _('Pending')),
        (CommunicationRequestsStatus.STARTED, _('Started')),
        (CommunicationRequestsStatus.SUCCESS, _('Success')),
        (CommunicationRequestsStatus.RETRYING, _('Retrying')),
        (CommunicationRequestsStatus.FAILED, _('Failed')),
    )
    task_id = models.UUIDField(default=uuid.uuid4, editable=False)
    communication_event = models.ForeignKey(CommunicationEvents, on_delete=models.DO_NOTHING, db_index=False)
    communication_type = models.CharField(
        max_length=255,
        choices=get_all_communications_choices(),
        default=CommunicationTypes.EMAIL
    )
    status = models.CharField(choices=status_choices, default=CommunicationRequestsStatus.PENDING, max_length=55)
    recipients = models.CharField(max_length=255)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    next_attempt_time = models.DateTimeField(null=True)
    result = models.TextField(null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)
    retries = models.IntegerField(default=0)
    retries_reasons = models.TextField(default=list)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, db_index=False)

    def __str__(self):
        return f'{str(self.communication_event)} - {self.task_id} - {self.status}'

    class Meta:
        db_table = 'communication_requests'
        ordering = ('-created_at',)
        verbose_name = _('Communication Request')
        verbose_name_plural = _('Communication Requests')
        indexes = [
            models.Index(fields=['created_at', 'user']),
        ]


