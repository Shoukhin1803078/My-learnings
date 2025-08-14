from rest_framework.views import APIView
from . models import Person
from .serializers import PersonSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class PersonAPIView(APIView):
    def get(self, request):
        person=Person.objects.all() # select *
        serializer=PersonSerializer(person,many=True)
        # print(serializer)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer=PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class SinglePersonAPIView(APIView):
    
    def get (self, request, pk):
        person=Person.objects.get(pk=pk)
        serializer=PersonSerializer(person)
        return Response (serializer.data)
    
    def put(self,request,pk):
        person=Person.objects.get(pk=pk)
        serializer=PersonSerializer(person,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        person=Person.objects.get(pk=pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



        







