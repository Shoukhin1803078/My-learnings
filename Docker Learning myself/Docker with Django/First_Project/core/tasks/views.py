from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer

class TasksAPI(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()