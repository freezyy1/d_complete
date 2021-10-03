from django.urls import path
from .views import NewList, NewDetailView, Search, NewCreateView, NewDeleteView, NewUpdateView, subscribe_me


urlpatterns = [
    path('', NewList.as_view()),
    path('<int:pk>', NewDetailView.as_view(), name='new'),
    path('search/', Search.as_view()),
    path('create/', NewCreateView.as_view(), name='new_create'),
    path('<int:pk>/update/', NewUpdateView.as_view(), name='new_update'),
    path('<int:pk>/delete/', NewDeleteView.as_view(), name='new_delete'),
    path('<int:pk>/subscribe/', subscribe_me, name='subscribe'),
]
