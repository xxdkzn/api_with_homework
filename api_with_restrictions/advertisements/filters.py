from django_filters import rest_framework as filters
from api_with_restrictions.advertisements.models import Advertisement

class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    title = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=[('OPEN', 'Открыто'), ('CLOSED', 'Закрыто')])
    created_at = filters.DateFromToRangeFilter()  # Фильтр для диапазона дат

    class Meta:
        model = Advertisement
        fields = ['title', 'status', 'created_at']  # created_at для фильтрации