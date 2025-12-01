from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError  # ДОДАНО ІМПОРТ

class Event(models.Model):
    EVENT_TYPES = [
        ('concert', 'Концерт'),
        ('festival', 'Фестиваль'),
        ('exhibition', 'Виставка'),
        ('master_class', 'Майстер-клас'),
        ('competition', 'Конкурс'),
        ('lecture', 'Лекція'),
        ('children', 'Дитяча подія'),
        ('other', 'Інше'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Назва події'
    )
    description = models.TextField(
        verbose_name='Опис події'
    )
    short_description = models.CharField(
        max_length=300,
        verbose_name='Короткий опис',
        blank=True
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name='Тип події'
    )
    start_date = models.DateTimeField(
        verbose_name='Дата та час початку'
    )
    end_date = models.DateTimeField(
        verbose_name='Дата та час завершення',
        blank=True,
        null=True
    )
    location = models.CharField(
        max_length=200,
        verbose_name='Місце проведення'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Ціна',
        default=0,
        validators=[MinValueValidator(0)]
    )
    max_participants = models.PositiveIntegerField(
        verbose_name='Максимальна кількість учасників',
        blank=True,
        null=True
    )
    current_participants = models.PositiveIntegerField(
        verbose_name='Поточна кількість учасників',
        default=0
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна подія'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Показувати на головній'
    )
    image = models.ImageField(
        upload_to='events/',
        verbose_name='Зображення',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Подія'
        verbose_name_plural = 'Події'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={'pk': self.pk})

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_sold_out(self):
        if self.max_participants:
            return self.current_participants >= self.max_participants
        return False

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError('Дата завершення не може бути раніше дати початку')
