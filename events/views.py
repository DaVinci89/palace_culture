from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.utils import timezone
import json
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True).order_by('-start_date')

        # Фільтрація за типом події
        event_type = self.request.GET.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        # Фільтрація за датою початку
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(start_date__date__gte=date_from)

        # Фільтрація за датою завершення
        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(start_date__date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо параметри фільтрів до контексту для відображення в шаблоні
        context['filters'] = {
            'event_type': self.request.GET.get('event_type', ''),
            'date_from': self.request.GET.get('date_from', ''),
            'date_to': self.request.GET.get('date_to', ''),
        }
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        return Event.objects.filter(is_active=True)


class EventCalendarView(TemplateView):
    template_name = 'events/event_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отримуємо події для календаря
        events = Event.objects.filter(is_active=True).order_by('start_date')

        # Форматуємо події для JavaScript
        calendar_events = []
        for event in events:
            calendar_events.append({
                'id': event.id,
                'title': event.title,
                'start': event.start_date.isoformat(),
                'end': event.end_date.isoformat() if event.end_date else event.start_date.isoformat(),
                'url': event.get_absolute_url(),
                'color': self.get_event_color(event.event_type),
                'extendedProps': {
                    'type': event.get_event_type_display(),
                    'type_key': event.event_type,
                    'location': event.location,
                    'price': float(event.price),
                }
            })

        # Конвертуємо в JSON без екранування HTML
        context['calendar_events'] = json.dumps(calendar_events, ensure_ascii=False)
        return context

    def get_event_color(self, event_type):
        colors = {
            'concert': '#3B82F6',  # синій
            'festival': '#EF4444',  # червоний
            'exhibition': '#10B981',  # зелений
            'master_class': '#F59E0B',  # жовтий
            'competition': '#8B5CF6',  # фіолетовий
            'lecture': '#6B7280',  # сірий
            'children': '#EC4899',  # рожевий
            'other': '#6366F1',  # індиго
        }
        return colors.get(event_type, '#6B7280')
