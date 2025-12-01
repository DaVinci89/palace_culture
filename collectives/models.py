from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import re

class Collective(models.Model):
    COLLECTIVE_TYPES = [
        ('dance', 'Танцювальний'),
        ('music', 'Музичний'),
        ('theater', 'Театральний'),
        ('other', 'Інший'),
    ]

    AGE_GROUPS = [
        ('children', 'Діти (4-10 років)'),
        ('kids', 'Діти (4-17 років)'),
        ('teens', 'Діти (5-17 років)'),
        ('adults', 'Дорослі (18+)'),
        ('seniors', 'Літні люди (60+)'),
        ('all', 'Всі вікові групи'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Назва колективу'
    )
    collective_type = models.CharField(
        max_length=20,
        choices=COLLECTIVE_TYPES,
        verbose_name='Тип колективу'
    )
    age_group = models.CharField(
        max_length=20,
        choices=AGE_GROUPS,
        verbose_name='Вікова група'
    )
    description = models.TextField(
        verbose_name='Опис колективу'
    )
    short_description = models.CharField(
        max_length=300,
        verbose_name='Короткий опис',
        blank=True
    )
    leader = models.CharField(
        max_length=100,
        verbose_name='Керівник'
    )
    leader_photo = models.ImageField(
        upload_to='collectives/leaders/',
        verbose_name='Фото керівника',
        blank=True
    )
    leader_description = models.TextField(
        verbose_name='Про керівника',
        blank=True
    )
    schedule = models.TextField(
        verbose_name='Розклад занять'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активний набір'
    )
    image = models.ImageField(
        upload_to='collectives/',
        verbose_name='Зображення',
        blank=True
    )
    youtube_url = models.URLField(
        verbose_name='YouTube посилання',
        blank=True
    )
    rating = models.FloatField(
        verbose_name='Рейтинг',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Колектив'
        verbose_name_plural = 'Колективи'
        ordering = ['name']
        indexes = [
            models.Index(fields=['collective_type', 'is_active']),
            models.Index(fields=['age_group', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collectives:collective_detail', kwargs={'pk': self.pk})

    # Додаємо метод для відгуків
    def get_reviews(self):
        return self.reviews.filter(is_approved=True)

    def get_youtube_id(self):
        """
        Витягує ID відео з YouTube URL
        """
        if not self.youtube_url:
            return None

        # Регулярний вираз для отримання ID з різних форматів YouTube URL
        regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(regex, self.youtube_url)

        if match:
            return match.group(1)
        return None


class CollectiveRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує розгляду'),
        ('approved', 'Підтверджено'),
        ('rejected', 'Відхилено'),
    ]

    collective = models.ForeignKey(
        Collective,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Гурток'
    )
    child_name = models.CharField(max_length=100, verbose_name="Ім'я дитини/учасника")
    child_age = models.PositiveIntegerField(verbose_name='Вік учасника')
    parent_name = models.CharField(max_length=100, verbose_name="Ім'я батька/опікуна")

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефону має бути в форматі: '+380501234567'"
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Номер телефону'
    )
    email = models.EmailField(verbose_name='Email адреса')
    notes = models.TextField(blank=True, verbose_name='Додаткові нотатки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус заявки'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заявка до гуртка'
        verbose_name_plural = 'Заявки до гуртків'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.child_name} - {self.collective.name}'


class Review(models.Model):
    collective = models.ForeignKey(
        Collective,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Гурток'
    )
    author_name = models.CharField(max_length=100, verbose_name="Ім'я автора")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг'
    )
    content = models.TextField(verbose_name='Відгук')
    is_approved = models.BooleanField(default=False, verbose_name='Опубліковано')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.collective.name}'
