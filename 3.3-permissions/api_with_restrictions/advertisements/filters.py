import django_filters
from django_filters.rest_framework import FilterSet
from advertisements.models import Advertisement


class AdvertisementFilter(FilterSet):
    """Фильтры для объявлений."""
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'status']
