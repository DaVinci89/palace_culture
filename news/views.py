from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import News, Tag, Comment, GalleryCategory, GalleryImage
from events.models import Event


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = News.objects.filter(is_published=True).order_by('-created_at')

        # Фільтрація за тегом
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)

        # Пошук
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(short_content__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['recent_news'] = News.objects.filter(is_published=True).order_by('-created_at')[:5]
        context['filters'] = {
            'tag': self.request.GET.get('tag', ''),
            'search': self.request.GET.get('search', ''),
        }
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_news'] = News.objects.filter(is_published=True).exclude(pk=self.object.pk).order_by(
            '-created_at')[:5]
        context['tags'] = self.object.tags.all()
        context['approved_comments'] = self.object.comments.filter(is_approved=True).order_by('-created_at')
        return context




class AddCommentView(DetailView):
    model = News
    template_name = 'news/add_comment.html'

    def post(self, request, *args, **kwargs):
        news = self.get_object()
        content = request.POST.get('content')

        if request.user.is_authenticated and content:
            Comment.objects.create(
                news=news,
                author=request.user,
                content=content,
                is_approved=True  # Модерація адміністратором
            )

        return redirect('news:news_detail', slug=news.slug)
