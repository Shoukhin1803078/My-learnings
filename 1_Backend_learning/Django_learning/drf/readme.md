# Drf folder tay way-2 use kore django project create kora sob jayagay

# **step-1**

- **python3 -m venv env
  source env/bin/activate**
- **pip install django
  pip install djangorestframework**

# **step-2: project create and going inside project**

**way-1 (with dot) :** i am inside a root folder . Now i wanna create a django project

```
cd root
python3 -m venv venv
source venv/bin/activate
django-admin startproject mydjangoproject .
```

```
Initial folder structure:

root/
    venv



After Creating django project Folder structure:
root/
    venv
    manage.py
    mydjangoproject
          __init__.py
          settings.py
          urls.py
          asgi.py
          wsgi.py
  
```

**way-2 (without dot ) :** i wanna create a folder and on that folder i wanna create a django project parallelly

- **django-admin startproject myproject**


```
Initial folder structure


root/
    venv
```


```
After creating djangoproject folder structure :

root/
    venv
    myproject/
             manage.py
             myproject/
                      __init__.py
                      settings.py
                      urls.py
                      asgi.py
                      wsgi.py
```

- **cd myproject**
- **python3 manage.py runserver**

# **Step-3: app create and add into INSTALLED_APPS for**

- > **python3 manage.py startapp myapp**
  >

```
venv
myproject/
    manage.py                # Command-line utility for admin tasks
    myproject/               # Project package
        __init__.py
        settings.py          # Project settings
        urls.py              # URL declarations
        asgi.py              # ASGI config for async servers
        wsgi.py              # WSGI config for traditional servers
    myapp/                   # Your application
        __init__.py
        admin.py             # Admin interface config
        apps.py              # App configuration
        models.py            # Data models
        views.py             # View functions/classes
        tests.py             # Tests
        migrations/          # Database migrations
```

External app "rest_framework" is also added. As we install djangorestframework in venv

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp1'
    "
]

```

- > **create urls.py in myapp**
  >

**myapp/urls.py--->**

```
from django.urls import path
from .views import SinglePersonAPIView,PersonAPIView

urlpatterns = [
    path('without_primary_key/', PersonAPIView.as_view()),
    path('with_primary_key/<int:pk>',SinglePersonAPIView.as_view())
]
```

**Include it into myproject/urls.py--->**

```
from django.contrib import admin
from django.urls import path,include
from myapp import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/',include("myapp.urls"))
]
```

# **Step-4 : CRUD_API Creation**

**myapp/model.py ---->**

```
from django.db import models

# Create your models here.
class Person(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=89)
```

**- > create serializers.py**

**myapp/serializers.py ---->**

```
from rest_framework import serializers 
from .models import Person

class PersonSerializer( serializers.ModelSerializer):
    class Meta:
        model=Person
        #fields=["first_name","last_name"]
        fields="__all__"
```

**Create CRUD API in  mapp/views.py----->**

```
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

```
