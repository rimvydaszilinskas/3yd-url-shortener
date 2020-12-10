from django.urls import path

from . import views


urlpatterns = [
    path('r/<str:short_id>/', views.redirect_to_url, name='trigger'),
    path('api/urls/', views.ShortURLListCreateAPI.as_view(), name='urls-view'),
    path('api/urls/<str:short_id>/',
         views.ShortURLRemoveAPI.as_view(), name='url-view'),
]
