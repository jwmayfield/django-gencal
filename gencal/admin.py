from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from forms import GenericCalendarAdminForm
from models import GenericCalendar

class GenericCalendarAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_content_types')
    prepopulated_fields = {"slug": ("name", )}
    form = GenericCalendarAdminForm 

admin.site.register(GenericCalendar, GenericCalendarAdmin)
