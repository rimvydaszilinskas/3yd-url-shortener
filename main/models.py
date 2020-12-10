from random import choice
from string import ascii_letters, digits
from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class ShortURL(models.Model):
    url = models.CharField(max_length=100)
    short_id = models.CharField(
        max_length=10, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    times_accessed = models.IntegerField(default=0)
    accessed_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True,
                               null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    @property
    def full_url(self):
        if not self.url.startswith('http://') and not self.url.startswith('https://'):
            return f'https://{self.url}'
        return self.url


@receiver(pre_save, sender=ShortURL)
def generate_short_id(sender, instance, *args, **kwargs):
    while instance.short_id is None or len(instance.short_id) == 0 or ShortURL.objects.filter(short_id=instance.short_id).exists():
        instance.short_id = ''.join(
            choice(ascii_letters+digits) for _ in range(7))
