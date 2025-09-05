from rest_framework import serializers
from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer): 
    # password = serializers.CharField(write_only=True, min_length=8) # write only mane holo password shudhu db te write kora jabe but read kora jabe na that means Objects.get_all() dile password bad e bakisob access/get korte parbo frontend theke otherwise na.
    password = serializers.CharField( min_length=8) # Eti use korle password ke read kora jabe through GET endpoint or password ke read kora jabe  

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    # # ----------------------------
    # # 🔹 Way 1: Manual + set_password()
    # # ----------------------------
    # def create(self, validated_data):
    #     # Step 1: Create user object without password
    #     user = User(
    #         username=validated_data["username"],
    #         email=validated_data["email"],
    #     )
    #     # Step 2: Hash the password safely
    #     user.set_password(validated_data["password"])
    #     # Step 3: Save user
    #     user.save()
    #     return user

    def create(self, d):
        # Step 1: Create user object without password
        user = User(
            username=d["username"],
            email=d["email"],
            # password=d["password"]
        )
        # Step 2: Hash the password safely
        user.set_password(d["password"])
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
    
    
  





# # ✅ Serializer to display user info safely
# class UserListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "email","password"]




# ---------------------------------------------------Class Concept -------------------------------------------------

# class A:
#     def __init__(self, tk,data):
#         self.tk=tk
#         self.data=data
    
#     def display(self):
#         print(f"tk===={self.tk} \n\ndata username====={self.data['username']}  email======{self.data['email']}")
    
# a=A(tk="50",data={"username":"abc","email":"shoukhin@gmail.com"})
# a.display()



