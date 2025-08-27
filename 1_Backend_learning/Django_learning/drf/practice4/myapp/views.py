from django.shortcuts import render
from rest_framework.views import APIView
from myapp.models import Person
from myapp.serializers import PersonSerializer

from rest_framework.response import Response
# Create your views here.
class PersonAPIView(APIView):
    def get(self,request):
        person=Person.objects.all()
        serializer=PersonSerializer(person,many=True)
        data=serializer.data 
        return Response(data)
    
    def post(self,request):
        serializer=PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"message":"error asshe"})
    