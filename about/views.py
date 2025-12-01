from django.views.generic import TemplateView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import HistoryTimeline, TeamMember, ContactInfo, Position
from .forms import ContactForm


class AboutView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history_events'] = HistoryTimeline.objects.all().order_by('-year', 'order')
        context['team_members'] = TeamMember.objects.filter(is_active=True).order_by('order', 'name')
        context['contact_info'] = ContactInfo.objects.first()
        return context


class ContactView(CreateView):
    template_name = 'about/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('about:contact_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        # Відправка email сповіщення
        subject = f'Нове повідомлення зворотного зв\'язку: {form.cleaned_data["subject"]}'
        message = f'''
        Нове повідомлення зворотного зв'язку:

        Ім'я: {form.cleaned_data['name']}
        Email: {form.cleaned_data['email']}
        Телефон: {form.cleaned_data['phone'] or 'Не вказано'}
        Тема: {form.cleaned_data['subject']}

        Повідомлення:
        {form.cleaned_data['message']}

        Час відправки: {self.object.created_at}
        '''

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        messages.success(self.request, 'Ваше повідомлення успішно відправлено! Ми зв\'яжемося з вами найближчим часом.')
        return response


class ContactSuccessView(TemplateView):
    template_name = 'about/contact_success.html'


class TeamView(TemplateView):
    template_name = 'about/team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Отримуємо активних співробітників, сортованих за відділом та порядком
        team_members = TeamMember.objects.filter(
            is_active=True,
            position__is_active=True
        ).select_related('position').order_by('position__department', 'order', 'name')

        # Групуємо співробітників за відділами
        departments = {
            'director': [],
            'creative': [],
            'technical': [],
        }

        for member in team_members:
            departments[member.position.department].append(member)

        context['team_members'] = team_members
        context['departments'] = departments
        return context


class TeamMemberDetailView(DetailView):
    model = TeamMember
    template_name = 'about/team_member_detail.html'
    context_object_name = 'member'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True).select_related('position')


class DetailView(TemplateView):
    template_name = 'about/detail.html'
