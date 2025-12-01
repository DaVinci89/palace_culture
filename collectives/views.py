from django.views.generic import ListView, DetailView, CreateView, View
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from .models import Collective, CollectiveRegistration, Review


class CollectiveListView(ListView):
    model = Collective
    template_name = 'collectives/collective_list.html'
    context_object_name = 'collectives'
    paginate_by = 12

    def get_queryset(self):
        queryset = Collective.objects.filter(is_active=True).order_by('name')

        # Фільтрація за типом гуртка
        collective_type = self.request.GET.get('collective_type')
        if collective_type:
            queryset = queryset.filter(collective_type=collective_type)

        # Фільтрація за віковою групою
        age_group = self.request.GET.get('age_group')
        if age_group:
            queryset = queryset.filter(age_group=age_group)

        # Пошук за назвою або керівником
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(leader__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = {
            'collective_type': self.request.GET.get('collective_type', ''),
            'age_group': self.request.GET.get('age_group', ''),
            'search': self.request.GET.get('search', ''),
        }
        return context


class CollectiveDetailView(DetailView):
    model = Collective
    template_name = 'collectives/collective_detail.html'
    context_object_name = 'collective'

    def get_queryset(self):
        return Collective.objects.filter(is_active=True)


class CollectiveRegistrationView(CreateView):
    model = CollectiveRegistration
    template_name = 'collectives/collective_registration.html'
    fields = ['collective', 'child_name', 'child_age', 'parent_name', 'phone', 'email', 'notes']
    success_url = reverse_lazy('collectives:registration_success')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Відправка email сповіщення
        collective = form.cleaned_data['collective']
        subject = f'Нова заявка до гуртка: {collective.name}'
        message = f'''
        Нова заявка до гуртка:

        Гурток: {collective.name}
        Учасник: {form.cleaned_data['child_name']}
        Вік: {form.cleaned_data['child_age']}
        Батько/опікун: {form.cleaned_data['parent_name']}
        Телефон: {form.cleaned_data['phone']}
        Email: {form.cleaned_data['email']}
        Нотатки: {form.cleaned_data['notes'] or 'Немає'}

        Заявка отримана: {self.object.created_at}
        '''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        messages.success(self.request, 'Ваша заявка успішно відправлена! Ми зв\'яжемося з вами найближчим часом.')
        return response


class CollectiveRegistrationSuccessView(DetailView):
    template_name = 'collectives/registration_success.html'

    def get_object(self):
        return None


class AddReviewView(View):
    def post(self, request, pk):
        collective = get_object_or_404(Collective, pk=pk)
        author_name = request.POST.get('author_name')
        rating = request.POST.get('rating')
        content = request.POST.get('content')

        # Створюємо відгук, але не публікуємо одразу (потрібна модерація)
        Review.objects.create(
            collective=collective,
            author_name=author_name,
            rating=rating,
            content=content,
            is_approved=False  # Модерація адміністратором
        )

        # Відправка email сповіщення про новий відгук
        subject = f'Новий відгук для гуртка: {collective.name}'
        message = f'''
        Новий відгук потребує модерації:

        Гурток: {collective.name}
        Автор: {author_name}
        Рейтинг: {rating}/5
        Відгук: {content}
        '''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        messages.success(request, 'Дякуємо за ваш відгук! Він буде опублікований після перевірки модератором.')
        return redirect('collectives:collective_detail', pk=pk)
