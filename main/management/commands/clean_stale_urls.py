from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from main.models import ShortURL


class Command(BaseCommand):
    help = 'Clean stale urls'

    def handle(self, *args, **kwargs):
        ShortURL.objects.filter(
            Q(Q(accessed_at__lte=timezone.now() - timedelta(days=30)) | Q(accessed_at__isnull=True, created_at__lte=timezone.now() - timedelta(days=30)), author__isnull=True) | Q(
                Q(accessed_at__lte=timezone.now() - timedelta(days=60)) | Q(accessed_at__isnull=True, created_at__lte=timezone.now() - timedelta(days=30)), times_accessed__lte=2, author__isnull=False)).update(deleted_at=timezone.now())
