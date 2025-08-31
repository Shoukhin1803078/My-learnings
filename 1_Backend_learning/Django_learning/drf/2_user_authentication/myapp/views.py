from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from rest_framework import status, permissions,authentication  #status -----→ HTTP codes like 200_OK, 400_BAD_REQUEST.  permissions --------→ who’s allowed (e.g., IsAuthenticated, AllowAny). authentication ---------→ how to check user identity (Token, Session, etc.).
from rest_framework.authtoken.models import Token


from .models import Name
from .serializers import NameSerializer
from .serializers import SignupSerializer








from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from rest_framework.authtoken.models import Token

from .serializers import SignupSerializer





class NameAPIView(APIView):
    def get(self,request):
        queryset=Name.objects.all()
        serializer=NameSerializer(queryset,many=True)
        data=serializer.data
        print(f"get data===={data}")
        # return Response(data,status=status.HTTP_200_OK)
        return Response({
            "data":data,
            "status": status.HTTP_200_OK,
            "hello_world":"Hi this is alamin . Hellow world"
            })
    def post(self,request):
        # data=request.data
        serializer=NameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            print(f"post data===={data}")
            # return Response (data,status=status.HTTP_201_CREATED)
            return Response({
                "data":data,
                "status": status.HTTP_201_CREATED,
                "hello_world":"Hi this is alamin . Hellow world",
                "message":"your object is created successfully"
            })
        else:
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        

# class SignupView(APIView):
#     permission_classes=[permissions.AllowAny] # anyone can hit this endpoint No login needed to sign up.
    
# def post(self, request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#             },
#             "token": token.key,
#         }, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#     # ## second-way:simplified version
#     # def post(self, request):
#     #     serializer = SignupSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)   # auto-returns 400 if invalid

#     #     user = serializer.save()
#     #     token, _ = Token.objects.get_or_create(user=user) #Duita value (token_instance, created_boolean) return korbe ei get_or_create method ta .  tries to find an existing token for that user. So return value is a touple (token_instance, created_boolean). 1.If found --------→ returns (token, False). 2.If not found ---------→ creates a new token and returns (token, True). 
#     #                                                     # # Step 1: Try to fetch or create a token for the given user
#     #                                                     # result = Token.objects.get_or_create(user=user)

#     #                                                     # # Step 2: The result is a tuple -> (token_object, created_boolean)
#     #                                                     # token_object = result[0]     # the actual Token model instance
#     #                                                     # created_flag = result[1]     # True if new token created, False if already existed

#     #                                                     # # Step 3: Assign like the original line did
#     #                                                     # token = token_object
#     #                                                     # _ = created_flag   # underscore is convention for "ignore this"
#     #     return Response({
#     #         "user": {
#     #             "id": user.id,
#     #             "username": user.username,
#     #             "email": user.email,
#     #         },
#     #         "token": token.key,
#     #     }, status=status.HTTP_201_CREATED)








class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "token": token.key,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "username and password required"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class TestTokenView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Token works ✨",
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        })


class LogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
