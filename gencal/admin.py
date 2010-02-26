from django.contrib import admin

from forms import GenericCalendarAdminForm
from models import GenericCalendar

class GenericCalendarAdmin(admin.ModelAdmin):
    filter_horizontal = ('content_types',)
    form = GenericCalendarAdminForm 
    list_display = ('name', 'slug', 'get_content_types')
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(GenericCalendar, GenericCalendarAdmin)
