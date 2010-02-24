from django import forms 
from django.contrib.contenttypes.models import ContentType

from models import GenericCalendar

class ContentTypeModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """ A more verbose ModelMultipleChoiceField for ContentTypes """
    def label_from_instance(self, obj):
        return '%s (%s.%s)' % (obj.name.title(), obj.app_label, obj.model)

class GenericCalendarAdminForm(forms.ModelForm):
    """ form to override the ContentType select field """
    content_types = ContentTypeModelMultipleChoiceField(queryset=ContentType.objects.all())

    class Meta:
        model = GenericCalendar

