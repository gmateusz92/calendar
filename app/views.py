from django.shortcuts import render
from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .models import *
from .utils import Calendar
from django.views.generic import ListView
from .forms import EventForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

def index(request):
    return render(request, 'index.html')


class CalendarView(ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def add_event(request):
    if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = EventForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                newevent = form.save(commit=False)
                newevent.save()
                # redirect to a new URL:
               # return redirect('index')
                return redirect('index')
            # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm()

    return render(request, 'add_event.html', {'form': form})


# def add_event(request):
#     form = EventForm(request.POST or None)
#     if request.POST and form.is_valid():
#         title = form.cleaned_data["title"]
#         description = form.cleaned_data["description"]
#         start_time = form.cleaned_data["start_time"]
#         end_time = form.cleaned_data["end_time"]
#         Event.objects.get_or_create(
#
#             title=title,
#             description=description,
#             start_time=start_time,
#             end_time=end_time,
#         )
#         return redirect('index')
#         #return HttpResponseRedirect(reverse("calendarapp:calendar"))
#     return render(request, "add_event.html", {"form": form})


def add_event(request):
    if request.method == 'GET':
        return render(request, 'add_event.html', {'form':EventForm()})
    else:
        try:
            form = EventForm(request.POST)
            newevent = form.save(commit=False)
            newevent.save()
            return redirect('index')
        except ValueError:
            return render(request, 'add_event.html', {'form':EventForm(), 'error':'Bad data passed in. Try again.'})