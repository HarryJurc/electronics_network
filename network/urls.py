from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NetworkLinkViewSet

# Создаем роутер и регистрируем наш ViewSet
router = DefaultRouter()
router.register(r'network-links', NetworkLinkViewSet, basename='networklink')

urlpatterns = [
    path('', include(router.urls)),
]
