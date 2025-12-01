from django.views.generic import TemplateView
from events.models import Event
from collectives.models import Collective
from news.models import News


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Події для слайдера (топ-події з is_featured=True)
        context['slider_events'] = Event.objects.filter(
            is_active=True,
            is_featured=True
        ).order_by('-start_date')[:5]  # Обмежуємо 5 подіями для слайдера

        # Останні новини для блоку "Актуальні новини"
        context['latest_news'] = News.objects.filter(
            is_published=True
        ).order_by('-created_at')[:3]

        # Популярні гуртки для блоку "Наші гуртки"
        context['featured_collectives'] = Collective.objects.filter(
            is_active=True
        ).order_by('-rating')[:8]

        return context
