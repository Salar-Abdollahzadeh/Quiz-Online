import django_filters
from .models import Track


class TrackFilter(django_filters.FilterSet):
    class Meta:
        model = Track
        fields = {
            "active": ["exact"],
            "name": ["icontains"],
            "singers__first_name": ["icontains"]
        }
