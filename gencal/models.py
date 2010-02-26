import datetime
from django.core.exceptions import FieldError
from django.db import models
from django.contrib.contenttypes.models import ContentType

from templatetags.gencal import ListCalendar
#TODO: Would it make more sense for ListCalendar to be defined here?

class GenericCalendar(models.Model):
    """
    The Generic Calendar allows us to create a named grouping of
    other models that should be displayed on a calendar. 
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content_types = models.ManyToManyField(ContentType)

    def __unicode__(self):
        return self.name

    def get_content_types(self):
        return "%s" % ', '.join([t.name for t in self.content_types.all()])

    def get_objects_for_date(self, year=None, month=None, day=None):
        """
        This method retrieves all of the objects associated with 
        content_types for the given date.

        #TODO: this currently ignores the day keyword. I'm still
        not sure if/how that should be handled.

        :keyword year: The year to which objects are associated.
        :type year: int.
        :keyword month: The month to which objects are associated.
        :type: int.
        """
        today = datetime.date.today()
        if year is None: year = today.year
        if month is None: month = today.month
        #if day is None: day = today.day
        obj_list = []
        for ct in self.content_types.all():
            try:
                obj_list += list(ct.model_class().objects.filter(date__year=year, date__month=month))
            except FieldError:
                field_name = get_date_attr_name(ct.model_class())
                if field_name:
                    ykey = "%s__year" % field_name
                    mkey = "%s__month" % field_name
                    obj_list += list(ct.model_class().objects.complex_filter({ykey: year, mkey: month}))
       
        return obj_list

def get_date_attr_name(cls):
    """
    Given a subclass of django.db.models.Model, this function
    inspects its fields to if it contains a DateField. If so,
    the field's name is returned. If the class does not contain
    a DateField, this function looks for a DateTimeField and 
    returns its name, instead.

    Caveat: This function will return the FIRST DateField 
    (or DateTimeField) found, which may not be the correct field.
    
    :param cls: A Class to inspect for a DateField or DateTimeField.
    :type cls: class.
    """
    for f in cls._meta.fields:
        if f.__class__.__name__ == "DateField":
            return f.name

    # if there's no DateField, try a DateTimeField
    for f in cls._meta.fields:
        if f.__class__.__name__ == "DateTimeField":
            return f.name

    return None

class GenericListCalendar(ListCalendar):
    """
    This class extends django-gencal's ListCalendar so that it expects 
    the results from the GenericCalendar.get_objects_for_date method.

    :param cal_items: A list of items to put in the calendar.
    :type cal_items: list.
    :keyword year: Year to render.
    :type year: int.
    :keyword month: Month to render.
    :type month: int.
    """
    def __init__(self, cal_items, year=None, month=None, *args, **kwargs):
        """
        Make sure month_dict contains the correct objects. To do this, it needs
        to call "get_date_attr_name" to so it looks at the correct field
        """
        # Pass the parent __init__ an empty list, since we'll fill in the correct values below.
        super(GenericListCalendar, self).__init__([], year, month, *args, **kwargs)

        for item in cal_items:
            date_attr = get_date_attr_name(item.__class__)
            date = getattr(item, date_attr, None)
            if type(date) == datetime.datetime:
                date = date.date()
            if date:
                self.month_dict[date].append(item)

    def formatday(self, day, weekday):
        """
        For each day (table cell) in the calendar, the following will be printed:
        - a hyperlink for each object (using the get_absolute_url if it is available)
        - the text of the above link will be displayed by calling the object's __unicode__ method.
        
        :arg day: A day to be formatted.
        :type day: date object.
        :arg weekday: Weekday of a given day.
        :type weekday: int.
        """
        link = self.get_link(day)
        day_content = '%d' % day.day
        if link:
            day_content = '<a href="%s">%d</a>' % (self.get_link(day), day.day)
        
        html_content = '%s' % day_content
        if len(self.month_dict[day]) > 0:
            html_content += '<ul>'
            for obj in self.month_dict[day]:
                try:
                    html_content += '<li><a href="%s">%s</a></li>' % (obj.get_absolute_url(), obj)
                except AttributeError:
                    # probably no get_absolute_url method.
                    html_content += '<li>%s</li>' % obj
            html_content += '</ul>'
        
        return '<td>%s</td>' % html_content

    def get_link(self, dt):
        return None
