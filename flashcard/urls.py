from django.urls import path
from . import views


urlpatterns = [
    path('novo/', views.novo_flashcard, name='novo_flashcard'),
]
