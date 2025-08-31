from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Name



class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Name
        fields="__all__"
        
        

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "password", "email")
        
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True}
        }
        
        
    ## create_user() is a shortcut that calls set_password() under the hood. Ei method o under the hood e set_password method use kore password  er khtre 
    
    # def create(self, validated_data):
    #     # hash password properly
    #     user = User.objects.create_user(
    #         username=validated_data["username"],
    #         email=validated_data.get("email", ""),
    #         password=validated_data["password"],
    #     )
    #     return user
    
    

    def create(self, validated_data):
        # ⚡ Step 1: create user object WITHOUT setting password yet
        # Here we manually build the User object
        # but DON'T assign password directly, otherwise it stays in plain text.
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )

        # ⚡ Step 2: hash the password safely
        # set_password() → hashes the raw password into a secure hash (PBKDF2 by default)
        user.set_password(validated_data["password"])

        # ⚡ Step 3: save user to DB (username + hashed password stored)
        user.save()

        return user
