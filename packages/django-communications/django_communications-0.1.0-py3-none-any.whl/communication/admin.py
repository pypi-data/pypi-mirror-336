from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib import admin
from django.utils import timezone

from .formsets import CommunicationEventsConfigurationsInlineFormSet
from .models import CommunicationEvents, CommunicationEventsConfigurations, CommunicationRequest


class CommunicationEventsConfigurationsInline(admin.TabularInline):
    model = CommunicationEventsConfigurations
    extra = 1
    formset = CommunicationEventsConfigurationsInlineFormSet


@admin.register(CommunicationEvents)
class CommunicationEventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')
    search_fields = ('name', 'code')
    inlines = [CommunicationEventsConfigurationsInline]


@admin.register(CommunicationRequest)
class CommunicationRequestAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'communication_event', 'communication_type', 'task_created_at', 'task_last_updated_at',
                    'status', 'user',)
    list_filter = (
        'status', 'communication_type', 'communication_event', 'user',
    )
    list_select_related = ('communication_event', 'user')
    date_hierarchy = 'created_at'

    def get_list_display(self, request):
        user_timezone = settings.TIME_ZONE

        if user_timezone:
            try:
                tz = ZoneInfo(user_timezone)
                timezone.activate(tz)
            except Exception as e:
                timezone.activate(ZoneInfo("UTC"))

        return super().get_list_display(request)

    def task_created_at(self, obj):
        if not obj.created_at:
            return None
        created_at = obj.created_at
        if timezone.is_naive(created_at):
            created_at = timezone.make_aware(created_at, timezone.get_default_timezone())
        return created_at.astimezone(timezone.get_current_timezone())
    task_created_at.short_description = 'Created at'

    def task_last_updated_at(self, obj):
        if not obj.updated_at:
            return None
        updated_at = obj.updated_at
        if timezone.is_naive(updated_at):
            updated_at = timezone.make_aware(updated_at, timezone.get_default_timezone())
        return updated_at.astimezone(timezone.get_current_timezone())
    task_last_updated_at.short_description = 'Last Updated at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def row_actions(self, obj):
    #     def get_retry_button():
    #         retry_url = reverse('retry_communication_request', kwargs={'communication_request_id': obj.pk})
    #         return format_html(
    #             '<a class="button" href="{}" title="{}">'
    #             '<i class="fa fa-history" aria-hidden="true"></i>'
    #             '</a>',
    #             retry_url,
    #             _("Retry Communication")
    #         )
    #
    #     if obj.status in [FAILURE_STATUS]:
    #         return get_retry_button()
    #
    #     return None
