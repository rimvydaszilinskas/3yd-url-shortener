from django.db.models import F
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone

from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView,
    RetrieveDestroyAPIView,
)

from .models import ShortURL
from .serializers import ShortURLSerializer


def redirect_to_url(request, *args, **kwargs):
    short_url = get_object_or_404(
        ShortURL, short_id=kwargs['short_id'], deleted_at__isnull=True)

    short_url.accessed_at = timezone.now()
    short_url.times_accessed = F('times_accessed') + 1
    short_url.save(update_fields=['accessed_at', 'times_accessed'])

    return redirect(short_url.full_url)


class ShortURLListCreateAPI(ListCreateAPIView):
    serializer_class = ShortURLSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShortURL.objects.filter(author=self.request.user, deleted_at__isnull=True)
        return ShortURL.objects.none()


class ShortURLRemoveAPI(RetrieveDestroyAPIView):
    lookup_field = 'short_id'
    serializer_class = ShortURLSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShortURL.objects.filter(author=self.request.user, deleted_at__isnull=True)
        return ShortURL.objects.none()
