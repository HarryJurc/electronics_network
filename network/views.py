from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import NetworkLink
from .serializers import NetworkLinkSerializer
from .permissions import IsActiveStaff


class NetworkLinkViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для работы со звеньями сети.
    Предоставляет полный CRUD.
    Возможна фильтрация по стране (?country=НАЗВАНИЕ_СТРАНЫ).
    """
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsActiveStaff]

    # Подключаем бэкенд для фильтрации
    filter_backends = [DjangoFilterBackend]
    # Указываем поля для фильтрации
    filterset_fields = ['country']
