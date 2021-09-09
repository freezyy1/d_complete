from django.urls import path
from .views import ProductList, ProductDetail

urlpatterns = [
    path('', ProductList.as_view()),
    path('<int:pk>', ProductDetail.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
]
