from django.urls import path
from .views import WebScrapingView

urlpatterns = [
    path('scrape-and-answer/', WebScrapingView.as_view(), name='scrape-and-answer'),
]