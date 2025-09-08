from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from accounts.serializers import SignupSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status


#-----------signup-----------------
class SignupView(APIView):
    def post(self,request):
        d=request.data # eti ekti dictionary 
        # -------------------way-2 (keyword argument passing approach)---------------
        serializer=SignupSerializer(data=d)
        if serializer.is_valid():
            serializer.save()
            # user_data=serializer.data
            return Response({
                "message":"user create hoyese",
                "user_data":serializer.data,
                "status":status.HTTP_201_CREATED
            })
        else:
            return Response({
                "error":serializer.error,
                "status":status.HTTP_400_BAD_REQUEST
            })

# --------------Admin Manage all users-------------

class AdminUserListView(APIView):
    
    
