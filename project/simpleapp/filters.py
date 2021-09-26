from django_filters import FilterSet, CharFilter
from .models import New


# создаём фильтр
class PostFilter(FilterSet):
    class Meta:
        model = New
        fields = ('author', 'post_name', 'created', 'rating_new',)
