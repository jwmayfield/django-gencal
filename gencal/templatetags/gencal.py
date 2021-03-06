from calendar import HTMLCalendar
from datetime import datetime

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.datastructures import SortedDict

register = template.Library()

@register.simple_tag
def gencal(obj_list, slug=None, year=None, month=None, calendar_class=None):
    """
    Renders a simple calendar of the given month and year if none are
    specified. Accomplishes this by passing the arguments to
    :class:`ListCalendar`

    ::

      {% gencal queryset %}

      {% gencal queryset 1983 12 %}
      

    :param obj_list: A list of objects to render on the calendar.
    :type obj_list: list.
    :keyword year: Year to render.
    :type year: int.
    :keyword month: Month to render.
    :type month: int.
    :returns: calendar as HTML
    :rtype: str.
    """
    today = datetime.today()
    if not year:
        year = today.year
    if not month:
        month = today.month
    if not calendar_class:
        calendar_class = ListCalendar
    return calendar_class(obj_list, year, month).formatmonth(slug, year, month)

class ListCalendar(HTMLCalendar):
    """
    This is a calendar object which accepts a ``list`` argument and a
    ``date_field`` keyword argument.. This class will return an HTML
    calendar with links on the days that are present in the list,
    using ``date_field`` as the lookup.

    It's assumed that the provided list is valid for the given month,
    ie: contains no outside dates.

    Usage::

        >>> from datetime import datetime, timedelta
        >>> from gencal.templatetags.gencal import ListCalendar
        >>> subclass = type('SubListClass', (ListCalendar,),{}) # This is equivalent to a subclass
        >>> subclass.get_link(self, dt) = lambda dt: "/items/%d/%d/%d" % (dt.year, dt.month, dt.day)
        >>> dates = [{'date':datetime.now(), 'name':'test'},
        ... {'date':datetime.now() + timedelta(days=5), 'name':'test2'}]
        >>> lc = subclass(dates)
        >>> print "".join(lc.formatmonth(2009, 01))
        <table border="0" cellpadding="0" cellspacing="0" class="month">
        <tr><th colspan="7" class="month">January 2009</th></tr>
        <tr><th class="mon">Mon</th><th class="tue">Tue</th><th class="wed">Wed</th><th class="thu">Thu</th><th class="fri">Fri</th><th class="sat">Sat</th><th class="sun">Sun</th></tr>
        <tr><td><a href="/items/2008/12/29">29</a></td><td><a href="/items/2008/12/30">30</a></td><td><a href="/items/2008/12/31">31</a></td><td><a href="/items/2009/1/1">1</a></td><td><a href="/items/2009/1/2">2</a></td><td><a href="/items/2009/1/3">3</a></td><td><a href="/items/2009/1/4">4</a></td></tr>
        <tr><td><a href="/items/2009/1/5">5</a></td><td><a href="/items/2009/1/6">6</a></td><td><a href="/items/2009/1/7">7</a></td><td><a href="/items/2009/1/8">8</a></td><td><a href="/items/2009/1/9">9</a></td><td><a href="/items/2009/1/10">10</a></td><td><a href="/items/2009/1/11">11</a></td></tr>
        <tr><td><a href="/items/2009/1/12">12</a></td><td><a href="/items/2009/1/13">13</a></td><td><a href="/items/2009/1/14">14</a></td><td><a href="/items/2009/1/15">15</a></td><td><a href="/items/2009/1/16">16</a></td><td><a href="/items/2009/1/17">17</a></td><td><a href="/items/2009/1/18">18</a></td></tr>
        <tr><td><a href="/items/2009/1/19">19</a></td><td><a href="/items/2009/1/20">20</a></td><td><a href="/items/2009/1/21">21</a></td><td><a href="/items/2009/1/22">22</a></td><td><a href="/items/2009/1/23">23</a></td><td><a href="/items/2009/1/24">24</a></td><td><a href="/items/2009/1/25">25</a></td></tr>
        <tr><td><a href="/items/2009/1/26">26</a></td><td><a href="/items/2009/1/27">27</a></td><td><a href="/items/2009/1/28">28</a></td><td><a href="/items/2009/1/29">29</a></td><td><a href="/items/2009/1/30">30</a></td><td><a href="/items/2009/1/31">31</a></td><td><a href="/items/2009/2/1">1</a></td></tr>
        </table>

    :param cal_items: A list of items to put in the calendar.
    :type cal_items: list.
    :keyword year: Year to render.
    :type year: int.
    :keyword month: Month to render.
    :type month: int.
    """

    def __init__(self, cal_items, year=None, month=None, *args, **kwargs):
        firstweekday = getattr(settings, 'CALENDAR_FIRST_WEEKDAY', 6)

        today = datetime.today()
        self.today = today.date()

        if year == None:
            year = today.year
        self.year = year

        if not month:
            month = today.month
        self.month = month

        self.date_field = kwargs.pop('date_field', 'date')

        super(ListCalendar, self).__init__(firstweekday=firstweekday, *args, **kwargs)

        cal_arr = self.monthdatescalendar(year, month)
        month_dict = SortedDict()
        for week in cal_arr:
            for date in week:
                month_dict[date] = []

        for item in cal_items:
            if isinstance(item, dict):
                possible_date = item.get(self.date_field)
            else:
                possible_date = getattr(item, self.date_field)
            if type(possible_date) == datetime:
                # transform possible_date to a date, not a datetime
                possible_date = possible_date.date()
            if possible_date:
                month_dict[possible_date].append(item)
        self.month_dict = month_dict

    def formatday(self, day, weekday, template='gencal/formatday.html'):
        """
        Return a day as a table cell.

        :arg day: A day to be formatted.
        :type day: date object.
        :arg weekday: Weekday of given day.
        :type weekday: int.
        """
        if day.month == self.month:
            day_num = day.day
        else:
            day_num = 0
        return render_to_string(template,
                {'link': self.get_link(day), 'day': day_num,
                    'today': day == self.today})

    def get_link(self, dt):
        """
        Should return a url to a given date, as represented by ``dt``
        
        :arg dt: date to turn into a url
        :type dt: date/datetime
        """
        return None

    def monthdates2calendar(self, year, month):
        """
        Function returns a list containing a list of tuples
        (representing a week), the tuples represent a
        ``datetime.date`` for the given day and the weekday associated
        with it.

        This is something that ought to be implemented in core. We
        have monthdatescalendar, monthdayscalendar,
        monthdays2calendar, but no monthdates2calendar.

        :keyword year: Year to render.
        :type year: int.
        :keyword month: Month to render.
        :type month: int.
        :returns: Tuple of (datetime, weekday).
        :rtype: tuple(datetime, int)
        """
        return [[(dt, dt.weekday()) for dt in week] for week in self.monthdatescalendar(year, month)]

    def formatweek(self, theweek, template='gencal/formatweek.html'):
        """
        Return a complete week as a table row.
        """
        days = [self.formatday(d, wd) for (d, wd) in theweek]
        return render_to_string(template, {'days': days})

    def formatweekday(self, day, template='gencal/formatweekday.html'):
        """
        Return a weekday name as a table header.
        """
        from calendar import day_abbr
        return render_to_string(template,
                {'class': self.cssclasses[day], 'weekday': day_abbr[day]})

    def formatweekheader(self, template='gencal/formatweekheader.html'):
        """
        Return a header for a week as a table row.
        """
        weekdays = [self.formatweekday(i) for i in self.iterweekdays()]
        return render_to_string(template,
                {'weekdays': weekdays})

    def formatmonthname(self, theyear, themonth, withyear=True, prev='',
            next='', template='gencal/formatmonthname.html'):
        """
        Return a month name as a table row.
        """
        from calendar import month_name
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return render_to_string(template,
                {'month_name': s, 'prev_month_link': prev,
                    'next_month_link': next})

    def formatmonth(self, slug, theyear, themonth, withyear=True,
            template='gencal/formatmonth.html'):
        """
        Return a formatted month as a table.

        Overridden so weeks will use monthdates2calendar, so we have
        access to full date objects, rather than numbers.

        :arg theyear: Year of calendar to render.
        :type theyear: int.
        :arg themonth: Month of calendar to render
        :type themonth: int.
        :keyword withyear: If true, it will show the year in the header.
        :type withyear: bool.
        """
        weeks = [self.formatweek(week) for week in
                self.monthdates2calendar(theyear, themonth)]
        prev_month_link = '%s%d/%02d/' % (reverse('genericcalendar-default',
            args=[slug]), theyear if themonth - 1 >= 1 else theyear - 1,
            themonth - 1 if themonth - 1 >= 1 else 12)
        next_month_link = '%s%d/%02d/' % (reverse('genericcalendar-default',
            args=[slug]), theyear if themonth + 1 <= 12 else theyear + 1,
            themonth + 1 if themonth + 1 <= 12 else 1)
        return render_to_string(template,
                {'month_name': self.formatmonthname(theyear, themonth,
                    withyear=withyear, prev=prev_month_link,
                    next=next_month_link), 'week_header': self.formatweekheader(),
                    'weeks': weeks, 'prev_month_link': prev_month_link,
                    'next_month_link': next_month_link})
