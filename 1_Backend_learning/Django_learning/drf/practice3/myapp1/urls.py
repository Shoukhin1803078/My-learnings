from django.urls import path
from .views import SinglePersonAPIView,PersonAPIView

urlpatterns = [
    path('without_primary_key/', PersonAPIView.as_view()),
    path('with_primary_key/<int:pk>',SinglePersonAPIView.as_view())
]
