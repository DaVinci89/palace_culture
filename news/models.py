from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Назва тегу')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL-ідентифікатор')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-ідентифікатор')
    content = models.TextField(verbose_name='Зміст')
    short_content = models.CharField(max_length=300, verbose_name='Короткий опис', blank=True)
    image = models.ImageField(upload_to='news/', verbose_name='Зображення', blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='news', verbose_name='Теги')
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Новина'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    content = models.TextField(verbose_name='Коментар')
    is_approved = models.BooleanField(default=False, verbose_name='Підтверджено')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']

    def __str__(self):
        return f'Коментар від {self.author} до {self.news.title}'

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва категорії')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-ідентифікатор')
    description = models.TextField(blank=True, verbose_name='Опис')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категорія галереї'
        verbose_name_plural = 'Категорії галереї'
        ordering = ['name']

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва')
    image = models.ImageField(upload_to='gallery/', verbose_name='Зображення')
    description = models.TextField(blank=True, verbose_name='Опис')
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Категорія'
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gallery_images',
        verbose_name='Подія'
    )
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Зображення галереї'
        verbose_name_plural = 'Зображення галереї'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
