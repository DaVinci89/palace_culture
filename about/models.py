from time import timezone

from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils.text import slugify


class HistoryTimeline(models.Model):
    year = models.PositiveIntegerField(verbose_name='Рік')
    title = models.CharField(max_length=200, verbose_name='Заголовок події')
    description = models.TextField(verbose_name='Опис події')
    image = models.ImageField(upload_to='history/', verbose_name='Зображення', blank=True)
    is_important = models.BooleanField(default=False, verbose_name='Важлива подія')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок відображення')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Подія історії'
        verbose_name_plural = 'Події історії'
        ordering = ['year', '-order']

    def __str__(self):
        return f'{self.year} - {self.title}'



class Position(models.Model):
    """Модель для посад співробітників"""
    DEPARTMENT_CHOICES = [
        ('director', 'Керівництво'),
        ('creative', 'Творчий відділ'),
        ('technical', 'Технічний відділ'),
    ]

    name = models.CharField(max_length=100, verbose_name='Назва посади')
    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES,
        verbose_name='Відділ'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок відображення')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Посада'
        verbose_name_plural = 'Посади'
        ordering = ['department', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_department_display()})"


class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я та прізвище")
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name='Посада',
        related_name='team_members'
    )
    nickname = models.CharField(max_length=100, verbose_name="Нікнейм", default=timezone)
    bio = models.TextField(verbose_name='Біографія')
    short_bio = models.CharField(max_length=350, verbose_name='Коротка біографія', blank=True)
    photo = models.ImageField(upload_to='team/', verbose_name='Фото', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефону має бути в форматі: '+380501234567'"
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Номер телефону',
        blank=True
    )

    order = models.PositiveIntegerField(default=0, verbose_name='Порядок відображення')
    is_active = models.BooleanField(default=True, verbose_name='Працює')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, verbose_name='Slug to URL')


    class Meta:
        verbose_name = 'Співробітник'
        verbose_name_plural = 'Співробітники'
        ordering = ['position__department', 'order', 'name']

    def __str__(self):
        return f'{self.name} - {self.position.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nickname)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('about:team_member_detail', kwargs={'slug': self.slug})


class ContactInfo(models.Model):
    address = models.TextField(verbose_name='Адреса')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    work_hours = models.TextField(verbose_name='Години роботи')
    map_embed_code = models.TextField(verbose_name='Код для вставки карти', blank=True,
                                      help_text='HTML код для вставки карти Google Maps')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта',
                                   blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Довгота',
                                    blank=True, null=True)

    # Соціальні мережі
    facebook_url = models.URLField(verbose_name='Facebook', blank=True)
    instagram_url = models.URLField(verbose_name='Instagram', blank=True)
    youtube_url = models.URLField(verbose_name='YouTube', blank=True)
    telegram_url = models.URLField(verbose_name='Telegram', blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Контактна інформація'
        verbose_name_plural = 'Контактна інформація'

    def __str__(self):
        return 'Контактна інформація'

    def save(self, *args, **kwargs):
        # Забезпечуємо, що буде лише один запис контактної інформації
        if not self.pk and ContactInfo.objects.exists():
            return
        super().save(*args, **kwargs)


class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Повідомлення')
    is_processed = models.BooleanField(default=False, verbose_name='Оброблено')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка зворотного зв\'язку'
        verbose_name_plural = 'Заявки зворотного зв\'язку'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'
