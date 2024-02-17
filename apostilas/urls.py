from django.urls import path
from . import views


urlpatterns = [
    path('adicionar/', views.adicionar_apostilas, name='adicionar_apostilas'),
    path('apostila/<int:id>', views.apostila, name='apostila'),
]
