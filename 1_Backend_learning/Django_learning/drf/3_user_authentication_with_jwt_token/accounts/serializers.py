from rest_framework import serializers
from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    # ----------------------------
    # 🔹 Way 1: Manual + set_password()
    # ----------------------------
    def create(self, validated_data):
        # Step 1: Create user object without password
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        # Step 2: Hash the password safely
        user.set_password(validated_data["password"])
        # Step 3: Save user
        user.save()
        return user

    # ----------------------------
    # 🔹 Way 2: Using create_user() shortcut
    # ----------------------------
    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data["username"],
    #         email=validated_data.get("email", ""),
    #         password=validated_data["password"],  # will be hashed
    #     )
    #     return user


class UserSerializer(serializers.ModelSerializer):
    """To show safe response (hide password)."""

    class Meta:
        model = User
        fields = ["id", "username", "email"]
