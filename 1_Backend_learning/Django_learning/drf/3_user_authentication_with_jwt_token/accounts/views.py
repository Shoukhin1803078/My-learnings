from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SignupSerializer
# from .serializers import UserListSerializer
from django.contrib.auth.models import User


# ✅ Signup
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(f"serializer.data====={serializer.data}")
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {
                    "data==":serializer.data,
                    "status":status.HTTP_201_CREATED
                }
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = User.objects.all()
        serializer = SignupSerializer(users, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {
                "data==":serializer.data,
                "status":status.HTTP_201_CREATED
            }
            )


# ✅ Login
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)



# ✅ Protected route
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]   # Require valid JWT access token

    def get(self, request):
        user = request.user  # DRF automatically gets user from JWT token
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )


# ✅ Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
