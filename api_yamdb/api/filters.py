from django_filters.rest_framework import FilterSet, BaseInFilter, CharFilter

from reviews.models import Title


class CharFilterInFilter(BaseInFilter, CharFilter):
    pass


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='contains')
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )
    genre = CharFilterInFilter(
        field_name='genre__slug',
        lookup_expr='in'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre',)
