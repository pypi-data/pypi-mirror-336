from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class CommunicationEventsConfigurationsInlineFormSet(BaseInlineFormSet):
    """
    Custom formset to ensure that no `communication_type` is repeated within the same `CommunicationEvent`.
    """
    def clean(self):
        communication_types = []
        for form in self.forms:
            if form.cleaned_data:
                communication_type = form.cleaned_data.get('communication_type')
                if communication_type in communication_types:
                    raise ValidationError('Each communication event configuration must have a unique communication type.')
                communication_types.append(communication_type)
        return super().clean()