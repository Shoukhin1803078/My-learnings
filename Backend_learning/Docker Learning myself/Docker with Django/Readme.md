#  venv creation:
python -m venv venv
.\venv\Scripts\activate

#  Django install:
pip install django 

# Django project create:
django-admin startproject djangorest
cd djangorest
python manage.py runserver


#  Django rest Framework install
pip install djangorestframework
"rest_framework" ei app ta INSTALLED_APPS er moddhe add kore dite hobe 
path('api-auth/', include('rest_framework.urls')) urlpatterns e eita add kore dite hobe 

urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls'))
]


Ekhon python manage.py runserver 


# App Creation
python manage.py startapp drapi




# Serializer Theroy:

Complex Data ( model or table )---Serializer----> Native python datatype --------Render------> json data 

Example:
t=Teacher.objects.all() #complex data
s=TeacherSerializer(t)  #Native python datatype
j=JSONRenderer().render(serializer.data) # jsondata


# Model or Complex Data Creation and Migration:

class Aiquest(models.Model):
    teacher_name=models.CharField(max_length=255)
    course_name=models.CharField(max_length=20)
    course_duration=models.IntegerField()
    seat=models.IntegerField()

python3 manage.py makemigrations
python3 manage.py migrate



# Ei model ta admin e register korle admin e ei table/model ta dekhte parbo

from .models import Aiquest

@admin.register(Aiquest)
class AiquestAdmin(admin.ModelAdmin):
    list_display=['id','teacher_name','course_name','course_duration','seat']
    

admin pannel e model ta dekhar jonno admin pannel e dhukte hobe  dhukar jonno : 
Er por admin pannel create korlam
python manage.py createsuperuser 
python manage.py runserver
