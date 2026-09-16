from django.conf import settings
from django.db import models

COLOR_CHOICES = [
    ('yellow', 'Amarillo'),
    ('pink', 'Rosa'),
    ('blue', 'Celeste'),
    ('green', 'Verde'),
]


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Note(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
    )
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='yellow')
    tags = models.ManyToManyField(Tag, related_name='notes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
