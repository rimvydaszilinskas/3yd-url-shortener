from datetime import datetime

from django.http import Http404
from django.shortcuts import redirect
from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView,
    RetrieveDestroyAPIView,
)

from main.models import ShortURL
from main.serializers import ShortURLSerializer


def redirect_to_url(request):
    try:
        short_url = ShortURL.objects.get(short_id=request.GET['id'])
    except ShortURL.DoesNotExist:
        raise Exception

    short_url.accessed_at = datetime.now()
    short_url.times_accessed = short_url.times_accessed + 1
    short_url.save()

    return redirect(short_url.url)


class ShortURLListCreateAPI(ListCreateAPIView):
    serializer_class = ShortURLSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShortURL.objects.filter(author=self.request.user)
        else:
            return ShortURL.objects.none()


class ShortURLRemoveAPI(RetrieveDestroyAPIView):
    lookup_field = 'short_id'
    serializer_class = ShortURLSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShortURL.objects.filter(author=self.request.user)
        else:
            return ShortURL.objects.none()

