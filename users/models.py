from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.urls import reverse


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефону має бути в форматі: '+380501234567'"
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name='Номер телефону'
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата народження'
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        verbose_name='Аватар'
    )
    email_confirmed = models.BooleanField(
        default=False,
        verbose_name='Email підтверджений'
    )

    # Додаткові поля для профілю
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Біографія'
    )
    website = models.URLField(
        blank=True,
        verbose_name='Веб-сайт'
    )

    # Налаштування сповіщень
    email_notifications = models.BooleanField(
        default=True,
        verbose_name='Email сповіщення'
    )
    sms_notifications = models.BooleanField(
        default=False,
        verbose_name='SMS сповіщення'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
