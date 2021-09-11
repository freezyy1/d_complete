# from django.shortcuts import render
from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from .models import Product
from datetime import datetime


class ProductList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context[
            'value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context

# создаём представление в котором будет детали конкретного отдельного товара
class ProductDetail(DetailView):
    model = Product  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'product.html'  # название шаблона будет product.html
    context_object_name = 'product'  # название объекта. в нём будет