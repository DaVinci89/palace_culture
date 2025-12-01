from django.db import models

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
    title = models.CharField(max_length=200, verbose_name='Назва', blank=True)
    image = models.ImageField(upload_to='gallery/', verbose_name='Зображення')
    description = models.TextField(blank=True, verbose_name='Опис')
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Категорія'
    )
    event = models.ForeignKey(
        'gallery.GalleryImage',
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
