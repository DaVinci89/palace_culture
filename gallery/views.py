from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import GalleryCategory, GalleryImage
from events.models import Event

class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'images'
    paginate_by = 12

    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_published=True).select_related('category', 'event').order_by('-created_at')

        # Фільтрація за категорією
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(GalleryCategory, slug=category_slug)
            queryset = queryset.filter(category=category)

        # Фільтрація за подією
        event_id = self.request.GET.get('event')
        if event_id:
            event = get_object_or_404(Event, pk=event_id)
            queryset = queryset.filter(event=event)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GalleryCategory.objects.all()
        context['events'] = Event.objects.filter(is_active=True).order_by('-start_date')[:10]
        return context