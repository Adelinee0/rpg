from django_filters import FilterSet
import django_filters
from django.forms import DateTimeInput
from .models import CATEGORY_CHOICES

class AdvertFilter(FilterSet):

    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title',)

    category = django_filters.ChoiceFilter(
        choices=CATEGORY_CHOICES,
        label='Category')

    createDate = django_filters.DateFilter(
        field_name='createDate',
        lookup_expr='lt',
        label='Date',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'}))

class ResponseFilter(FilterSet):

    title = django_filters.CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='Title', )

    author = django_filters.CharFilter(
        field_name='authorResponse',
        lookup_expr='icontains',
        label='Author',
    )



