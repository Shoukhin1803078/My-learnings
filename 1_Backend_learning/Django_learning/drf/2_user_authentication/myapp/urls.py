
# from django.urls import path
# from .views import NameAPIView
# from .views import SignupView
# urlpatterns = [
#     path('myapp_crud/',NameAPIView.as_view()),
#     path('signup/',SignupView.as_view())
# ]


from django.urls import path
from .views import SignupView, LoginView, TestTokenView, LogoutView
from .views import NameAPIView

urlpatterns = [
    path('myapp_crud/',NameAPIView.as_view()),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("test-token/", TestTokenView.as_view(), name="test-token"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
