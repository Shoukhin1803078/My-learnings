from django.urls import path
from .views import SignupView, LoginView, LogoutView,ProfileView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),  # ✅ new protected route
    path("logout/", LogoutView.as_view(), name="logout"),
    
]
