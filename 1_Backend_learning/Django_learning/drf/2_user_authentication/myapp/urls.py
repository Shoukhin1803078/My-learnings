
from django.urls import path
from .views import NameAPIView
from .views import SignupView
urlpatterns = [
    path('myapp_crud/',NameAPIView.as_view()),
    path('signup/',SignupView.as_view())
]

