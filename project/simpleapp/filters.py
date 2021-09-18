from django_filters import FilterSet, CharFilter
from .models import New


# создаём фильтр
class PostFilter(FilterSet):
    user__author = CharFilter(lookup_expr='icontains')
    category__category = CharFilter(lookup_expr='icontains')
    # Здесь в мета классе надо предоставить модель и указать поля по которым будет
    # фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = New
        fields = ('author', 'post_name')
