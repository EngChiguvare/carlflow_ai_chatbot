from django.contrib import admin
from django.utils.html import format_html
from .models import Lead, Appointment

admin.site.site_header='carlflow_ai Administration'
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('phone', 'colored_status', 'score', 'created_at')
    list_filter = ('status',)
    search_fields = ('phone', 'message')

    def colored_status(self, obj):
        colors = {'HOT': 'red', 'WARM': 'orange', 'COLD': 'blue'}
        return format_html('<b style="color:{}">{}</b>', colors[obj.status], obj.status)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('lead', 'scheduled_for', 'confirmed', 'created_at')
    list_filter = ('confirmed',)