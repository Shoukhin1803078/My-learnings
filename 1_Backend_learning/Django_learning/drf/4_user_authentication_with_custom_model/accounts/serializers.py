from rest_framework import serializers
from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model=CustomUser
        field=["id","username","email","password","role"]
    
        def create(self,d):
            u=d['username']
            e=d['email']
            p=d['password']
            user=CustomUser(username=u,email=e)
            user.set_password(d['password'])
            user.save()
            return user
                
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        field=["id","username","email","role"]