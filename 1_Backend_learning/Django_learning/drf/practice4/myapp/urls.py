from django.urls import path
from myapp.views import PersonAPIView
urlpatterns = [
    path('without_primary_key/', PersonAPIView.as_view())
]