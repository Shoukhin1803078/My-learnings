 let’s build the **full role-based user management system** with **JWT + DRF** 🔥.

This will include:

* ✅ Custom User model with `role`
* ✅ Signup/Login
* ✅ Role-based endpoints (`admin`, `staff`, `user`)
* ✅ JWT authentication

# 📂 Project Structure

<pre class="overflow-visible!" data-start="282" data-end="438"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>project/
│── project/settings.py
│── accounts/
│    ├── models.py
│    ├── serializers.py
│    ├── permissions.py
│    ├── views.py
│    ├── urls.py</span></span></code></div></div></pre>



# 1️⃣ `accounts/models.py`

<pre class="overflow-visible!" data-start="472" data-end="862"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> django.db </span><span>import</span><span> models
</span><span>from</span><span> django.contrib.auth.models </span><span>import</span><span> AbstractUser


</span><span>class</span><span></span><span>CustomUser</span><span>(</span><span>AbstractUser</span><span>):
    ROLE_CHOICES = (
        (</span><span>"admin"</span><span>, </span><span>"Admin"</span><span>),
        (</span><span>"staff"</span><span>, </span><span>"Staff"</span><span>),
        (</span><span>"user"</span><span>, </span><span>"User"</span><span>),
    )
    role = models.CharField(max_length=</span><span>20</span><span>, choices=ROLE_CHOICES, default=</span><span>"user"</span><span>)

    </span><span>def</span><span></span><span>__str__</span><span>(</span><span>self</span><span>):
        </span><span>return</span><span></span><span>f"{self.username}</span><span> (</span><span>{self.role}</span><span>)"</span></span></code></div></div></pre>



# 2️⃣ `accounts/serializers.py`

<pre class="overflow-visible!" data-start="901" data-end="1533"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework </span><span>import</span><span> serializers
</span><span>from</span><span> .models </span><span>import</span><span> CustomUser


</span><span>class</span><span></span><span>SignupSerializer</span><span>(serializers.ModelSerializer):
    password = serializers.CharField(write_only=</span><span>True</span><span>, min_length=</span><span>8</span><span>)

    </span><span>class</span><span></span><span>Meta</span><span>:
        model = CustomUser
        fields = [</span><span>"username"</span><span>, </span><span>"email"</span><span>, </span><span>"password"</span><span>, </span><span>"role"</span><span>]

    </span><span>def</span><span></span><span>create</span><span>(</span><span>self, validated_data</span><span>):
        user = CustomUser(
            username=validated_data[</span><span>"username"</span><span>],
            email=validated_data.get(</span><span>"email"</span><span>, </span><span>""</span><span>),
            role=validated_data.get(</span><span>"role"</span><span>, </span><span>"user"</span><span>),
        )
        user.set_password(validated_data[</span><span>"password"</span><span>])
        user.save()
        </span><span>return</span><span> user</span></span></code></div></div></pre>



# 3️⃣ `accounts/permissions.py`

<pre class="overflow-visible!" data-start="1572" data-end="2105"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework.permissions </span><span>import</span><span> BasePermission


</span><span>class</span><span></span><span>IsAdmin</span><span>(</span><span>BasePermission</span><span>):
    </span><span>def</span><span></span><span>has_permission</span><span>(</span><span>self, request, view</span><span>):
        </span><span>return</span><span> request.user.is_authenticated </span><span>and</span><span> request.user.role == </span><span>"admin"</span><span>


</span><span>class</span><span></span><span>IsStaff</span><span>(</span><span>BasePermission</span><span>):
    </span><span>def</span><span></span><span>has_permission</span><span>(</span><span>self, request, view</span><span>):
        </span><span>return</span><span> request.user.is_authenticated </span><span>and</span><span> request.user.role == </span><span>"staff"</span><span>


</span><span>class</span><span></span><span>IsUser</span><span>(</span><span>BasePermission</span><span>):
    </span><span>def</span><span></span><span>has_permission</span><span>(</span><span>self, request, view</span><span>):
        </span><span>return</span><span> request.user.is_authenticated </span><span>and</span><span> request.user.role == </span><span>"user"</span></span></code></div></div></pre>





# 4️⃣ `accounts/views.py`

<pre class="overflow-visible!" data-start="2138" data-end="3477"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework.views </span><span>import</span><span> APIView
</span><span>from</span><span> rest_framework.response </span><span>import</span><span> Response
</span><span>from</span><span> rest_framework </span><span>import</span><span> status
</span><span>from</span><span> rest_framework.permissions </span><span>import</span><span> IsAuthenticated

</span><span>from</span><span> .serializers </span><span>import</span><span> SignupSerializer
</span><span>from</span><span> .permissions </span><span>import</span><span> IsAdmin, IsStaff, IsUser


</span><span># ✅ Signup</span><span>
</span><span>class</span><span></span><span>SignupView</span><span>(</span><span>APIView</span><span>):
    </span><span>def</span><span></span><span>post</span><span>(</span><span>self, request</span><span>):
        serializer = SignupSerializer(data=request.data)
        </span><span>if</span><span> serializer.is_valid():
            serializer.save()
            </span><span>return</span><span> Response(
                {</span><span>"message"</span><span>: </span><span>"User created successfully"</span><span>},
                status=status.HTTP_201_CREATED
            )
        </span><span>return</span><span> Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


</span><span># ✅ Admin-only endpoint</span><span>
</span><span>class</span><span></span><span>AdminOnlyView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsAdmin]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>f"Hello Admin {request.user.username}</span><span>!"})


</span><span># ✅ Staff-only endpoint</span><span>
</span><span>class</span><span></span><span>StaffOnlyView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsStaff]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>f"Hello Staff {request.user.username}</span><span>!"})


</span><span># ✅ User-only endpoint</span><span>
</span><span>class</span><span></span><span>UserOnlyView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsUser]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>f"Hello User {request.user.username}</span><span>!"})
</span></span></code></div></div></pre>

---

# 5️⃣ `accounts/urls.py`

<pre class="overflow-visible!" data-start="3509" data-end="4131"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> django.urls </span><span>import</span><span> path
</span><span>from</span><span> .views </span><span>import</span><span> SignupView, AdminOnlyView, StaffOnlyView, UserOnlyView
</span><span>from</span><span> rest_framework_simplejwt.views </span><span>import</span><span> TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(</span><span>"signup/"</span><span>, SignupView.as_view(), name=</span><span>"signup"</span><span>),
    path(</span><span>"login/"</span><span>, TokenObtainPairView.as_view(), name=</span><span>"login"</span><span>),
    path(</span><span>"token/refresh/"</span><span>, TokenRefreshView.as_view(), name=</span><span>"token_refresh"</span><span>),

    path(</span><span>"admin-area/"</span><span>, AdminOnlyView.as_view(), name=</span><span>"admin-area"</span><span>),
    path(</span><span>"staff-area/"</span><span>, StaffOnlyView.as_view(), name=</span><span>"staff-area"</span><span>),
    path(</span><span>"user-area/"</span><span>, UserOnlyView.as_view(), name=</span><span>"user-area"</span><span>),
]
</span></span></code></div></div></pre>

---

# 6️⃣ `project/settings.py`

Make sure you have these:

<pre class="overflow-visible!" data-start="4193" data-end="4483"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>INSTALLED_APPS = [
    ...
    </span><span>"rest_framework"</span><span>,
    </span><span>"rest_framework_simplejwt"</span><span>,
    </span><span>"accounts"</span><span>,
]

AUTH_USER_MODEL = </span><span>"accounts.CustomUser"</span><span>

REST_FRAMEWORK = {
    </span><span>"DEFAULT_AUTHENTICATION_CLASSES"</span><span>: (
        </span><span>"rest_framework_simplejwt.authentication.JWTAuthentication"</span><span>,
    )
}
</span></span></code></div></div></pre>

---

# 7️⃣ Migrate and Run

<pre class="overflow-visible!" data-start="4512" data-end="4616"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python manage.py makemigrations accounts
python manage.py migrate
python manage.py runserver
</span></span></code></div></div></pre>

---

# 🔥 Usage Flow

1. **Signup (choose role)**

   <pre class="overflow-visible!" data-start="4671" data-end="4826"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>POST /signup/
   {
     "username": "john",
     "email": "john@example.com",
     "password": "strongpass123",
     "role": "staff"
   }
   </span></code></div></div></pre>
2. **Login**

   <pre class="overflow-visible!" data-start="4844" data-end="4942"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>POST /login/
   {
     "username": "john",
     "password": "strongpass123"
   }
   </span></code></div></div></pre>

   → Returns `access` + `refresh` token.
3. **Use Access Token**

   <pre class="overflow-visible!" data-start="5012" data-end="5082"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>GET</span><span></span><span>/</span><span>staff</span><span>-</span><span>area</span><span>/</span><span>
   </span><span>Authorization</span><span>: Bearer </span><span><</span><span>access_token</span><span>></span><span>
   </span></span></code></div></div></pre>

   * `/admin-area/` → only `admin`
   * `/staff-area/` → only `staff`
   * `/user-area/` → only `user`

---

✅ Boom! Now you have a **full JWT + role-based user management system** 🎯.







👉 Do you want me to extend this further so that  **admins can list, update, and delete users** , while normal users can  **only see/edit their own profile** ?



Perfect bro 🔥 now let’s **extend the role-based system** so it looks more like a real-world user management system.

We’ll add:

* ✅ Admin: **can list, update, delete any user**
* ✅ Normal user: **can only view & update their own profile**
* ✅ Staff: (optional) can see all users but not edit/delete

---

## 1️⃣ Update `accounts/serializers.py`

We’ll add a `UserSerializer` for returning user details.

<pre class="overflow-visible!" data-start="414" data-end="1271"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework </span><span>import</span><span> serializers
</span><span>from</span><span> .models </span><span>import</span><span> CustomUser


</span><span>class</span><span></span><span>SignupSerializer</span><span>(serializers.ModelSerializer):
    password = serializers.CharField(write_only=</span><span>True</span><span>, min_length=</span><span>8</span><span>)

    </span><span>class</span><span></span><span>Meta</span><span>:
        model = CustomUser
        fields = [</span><span>"id"</span><span>, </span><span>"username"</span><span>, </span><span>"email"</span><span>, </span><span>"password"</span><span>, </span><span>"role"</span><span>]

    </span><span>def</span><span></span><span>create</span><span>(</span><span>self, validated_data</span><span>):
        user = CustomUser(
            username=validated_data[</span><span>"username"</span><span>],
            email=validated_data.get(</span><span>"email"</span><span>, </span><span>""</span><span>),
            role=validated_data.get(</span><span>"role"</span><span>, </span><span>"user"</span><span>),
        )
        user.set_password(validated_data[</span><span>"password"</span><span>])
        user.save()
        </span><span>return</span><span> user


</span><span>class</span><span></span><span>UserSerializer</span><span>(serializers.ModelSerializer):
    </span><span>"""Serializer for showing users (used by Admin/User profile)."""</span><span>

    </span><span>class</span><span></span><span>Meta</span><span>:
        model = CustomUser
        fields = [</span><span>"id"</span><span>, </span><span>"username"</span><span>, </span><span>"email"</span><span>, </span><span>"role"</span><span>]
</span></span></code></div></div></pre>

---

## 2️⃣ Update `accounts/views.py`

Add admin & user profile management endpoints.

<pre class="overflow-visible!" data-start="1360" data-end="3271"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework.views </span><span>import</span><span> APIView
</span><span>from</span><span> rest_framework.response </span><span>import</span><span> Response
</span><span>from</span><span> rest_framework </span><span>import</span><span> status
</span><span>from</span><span> rest_framework.permissions </span><span>import</span><span> IsAuthenticated

</span><span>from</span><span> .serializers </span><span>import</span><span> SignupSerializer, UserSerializer
</span><span>from</span><span> .permissions </span><span>import</span><span> IsAdmin, IsStaff, IsUser
</span><span>from</span><span> .models </span><span>import</span><span> CustomUser


</span><span># ✅ Signup</span><span>
</span><span>class</span><span></span><span>SignupView</span><span>(</span><span>APIView</span><span>):
    </span><span>def</span><span></span><span>post</span><span>(</span><span>self, request</span><span>):
        serializer = SignupSerializer(data=request.data)
        </span><span>if</span><span> serializer.is_valid():
            serializer.save()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"User created successfully"</span><span>}, status=status.HTTP_201_CREATED)
        </span><span>return</span><span> Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


</span><span># ✅ Admin: Manage all users</span><span>
</span><span>class</span><span></span><span>AdminUserListView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsAdmin]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        users = CustomUser.objects.</span><span>all</span><span>()
        serializer = UserSerializer(users, many=</span><span>True</span><span>)
        </span><span>return</span><span> Response(serializer.data)

    </span><span>def</span><span></span><span>delete</span><span>(</span><span>self, request, user_id</span><span>):
        </span><span>try</span><span>:
            user = CustomUser.objects.get(</span><span>id</span><span>=user_id)
            user.delete()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"User deleted"</span><span>}, status=status.HTTP_204_NO_CONTENT)
        </span><span>except</span><span> CustomUser.DoesNotExist:
            </span><span>return</span><span> Response({</span><span>"error"</span><span>: </span><span>"User not found"</span><span>}, status=status.HTTP_404_NOT_FOUND)


</span><span># ✅ User: Manage own profile</span><span>
</span><span>class</span><span></span><span>UserProfileView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsUser]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        serializer = UserSerializer(request.user)
        </span><span>return</span><span> Response(serializer.data)

    </span><span>def</span><span></span><span>put</span><span>(</span><span>self, request</span><span>):
        serializer = UserSerializer(request.user, data=request.data, partial=</span><span>True</span><span>)
        </span><span>if</span><span> serializer.is_valid():
            serializer.save()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"Profile updated"</span><span>, </span><span>"user"</span><span>: serializer.data})
        </span><span>return</span><span> Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
</span></span></code></div></div></pre>

---

## 3️⃣ Update `accounts/urls.py`

<pre class="overflow-visible!" data-start="3311" data-end="4254"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> django.urls </span><span>import</span><span> path
</span><span>from</span><span> .views </span><span>import</span><span> SignupView, AdminUserListView, UserProfileView, AdminOnlyView, StaffOnlyView, UserOnlyView
</span><span>from</span><span> rest_framework_simplejwt.views </span><span>import</span><span> TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(</span><span>"signup/"</span><span>, SignupView.as_view(), name=</span><span>"signup"</span><span>),
    path(</span><span>"login/"</span><span>, TokenObtainPairView.as_view(), name=</span><span>"login"</span><span>),
    path(</span><span>"token/refresh/"</span><span>, TokenRefreshView.as_view(), name=</span><span>"token_refresh"</span><span>),

    </span><span># Role-based endpoints</span><span>
    path(</span><span>"admin-area/"</span><span>, AdminOnlyView.as_view(), name=</span><span>"admin-area"</span><span>),
    path(</span><span>"staff-area/"</span><span>, StaffOnlyView.as_view(), name=</span><span>"staff-area"</span><span>),
    path(</span><span>"user-area/"</span><span>, UserOnlyView.as_view(), name=</span><span>"user-area"</span><span>),

    </span><span># User management</span><span>
    path(</span><span>"admin/users/"</span><span>, AdminUserListView.as_view(), name=</span><span>"admin-users"</span><span>),
    path(</span><span>"admin/users/<int:user_id>/"</span><span>, AdminUserListView.as_view(), name=</span><span>"admin-user-delete"</span><span>),
    path(</span><span>"me/"</span><span>, UserProfileView.as_view(), name=</span><span>"user-profile"</span><span>),
]
</span></span></code></div></div></pre>

---

## 4️⃣ 🔥 Usage Examples

### Signup user

<pre class="overflow-visible!" data-start="4303" data-end="4433"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>POST /signup/
{
  "username": "john",
  "email": "john@example.com",
  "password": "strongpass123",
  "role": "user"
}
</span></code></div></div></pre>

### Login

<pre class="overflow-visible!" data-start="4445" data-end="4525"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>POST /login/
{
  "username": "john",
  "password": "strongpass123"
}
</span></code></div></div></pre>

---

### Admin Actions

#### List all users

<pre class="overflow-visible!" data-start="4570" data-end="4635"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>GET /admin/users/
Authorization: Bearer <admin_token>
</span></code></div></div></pre>

#### Delete a user

<pre class="overflow-visible!" data-start="4656" data-end="4726"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>DELETE /admin/users/3/
Authorization: Bearer <admin_token>
</span></code></div></div></pre>

---

### User Actions

#### Get own profile

<pre class="overflow-visible!" data-start="4771" data-end="4826"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>GET /me/
Authorization: Bearer <user_token>
</span></code></div></div></pre>

#### Update own profile

<pre class="overflow-visible!" data-start="4852" data-end="4944"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>PUT /me/
Authorization: Bearer <user_token>
{
  "email": "newjohn@example.com"
}
</span></code></div></div></pre>


✅ Now we have a  **complete role-based user management system** :

* Admin can manage everyone 🔑
* User can only manage themselves 👤
* Staff can have their own restricted endpoints 👷

---

👉 Do you want me to also add **staff permissions** (like “staff can view all users but not delete/update”) to make it even closer to a real company-style system?














Perfect bro 🔥 now let’s **extend the role-based system** so it looks more like a real-world user management system.

We’ll add:

* ✅ Admin: **can list, update, delete any user**
* ✅ Normal user: **can only view & update their own profile**
* ✅ Staff: (optional) can see all users but not edit/delete

---

## 1️⃣ Update `accounts/serializers.py`

We’ll add a `UserSerializer` for returning user details.

<pre class="overflow-visible!" data-start="414" data-end="1271"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework </span><span>import</span><span> serializers
</span><span>from</span><span> .models </span><span>import</span><span> CustomUser


</span><span>class</span><span></span><span>SignupSerializer</span><span>(serializers.ModelSerializer):
    password = serializers.CharField(write_only=</span><span>True</span><span>, min_length=</span><span>8</span><span>)

    </span><span>class</span><span></span><span>Meta</span><span>:
        model = CustomUser
        fields = [</span><span>"id"</span><span>, </span><span>"username"</span><span>, </span><span>"email"</span><span>, </span><span>"password"</span><span>, </span><span>"role"</span><span>]

    </span><span>def</span><span></span><span>create</span><span>(</span><span>self, validated_data</span><span>):
        user = CustomUser(
            username=validated_data[</span><span>"username"</span><span>],
            email=validated_data.get(</span><span>"email"</span><span>, </span><span>""</span><span>),
            role=validated_data.get(</span><span>"role"</span><span>, </span><span>"user"</span><span>),
        )
        user.set_password(validated_data[</span><span>"password"</span><span>])
        user.save()
        </span><span>return</span><span> user


</span><span>class</span><span></span><span>UserSerializer</span><span>(serializers.ModelSerializer):
    </span><span>"""Serializer for showing users (used by Admin/User profile)."""</span><span>

    </span><span>class</span><span></span><span>Meta</span><span>:
        model = CustomUser
        fields = [</span><span>"id"</span><span>, </span><span>"username"</span><span>, </span><span>"email"</span><span>, </span><span>"role"</span><span>]
</span></span></code></div></div></pre>

---

## 2️⃣ Update `accounts/views.py`

Add admin & user profile management endpoints.

<pre class="overflow-visible!" data-start="1360" data-end="3271"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework.views </span><span>import</span><span> APIView
</span><span>from</span><span> rest_framework.response </span><span>import</span><span> Response
</span><span>from</span><span> rest_framework </span><span>import</span><span> status
</span><span>from</span><span> rest_framework.permissions </span><span>import</span><span> IsAuthenticated

</span><span>from</span><span> .serializers </span><span>import</span><span> SignupSerializer, UserSerializer
</span><span>from</span><span> .permissions </span><span>import</span><span> IsAdmin, IsStaff, IsUser
</span><span>from</span><span> .models </span><span>import</span><span> CustomUser


</span><span># ✅ Signup</span><span>
</span><span>class</span><span></span><span>SignupView</span><span>(</span><span>APIView</span><span>):
    </span><span>def</span><span></span><span>post</span><span>(</span><span>self, request</span><span>):
        serializer = SignupSerializer(data=request.data)
        </span><span>if</span><span> serializer.is_valid():
            serializer.save()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"User created successfully"</span><span>}, status=status.HTTP_201_CREATED)
        </span><span>return</span><span> Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


</span><span># ✅ Admin: Manage all users</span><span>
</span><span>class</span><span></span><span>AdminUserListView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsAdmin]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        users = CustomUser.objects.</span><span>all</span><span>()
        serializer = UserSerializer(users, many=</span><span>True</span><span>)
        </span><span>return</span><span> Response(serializer.data)

    </span><span>def</span><span></span><span>delete</span><span>(</span><span>self, request, user_id</span><span>):
        </span><span>try</span><span>:
            user = CustomUser.objects.get(</span><span>id</span><span>=user_id)
            user.delete()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"User deleted"</span><span>}, status=status.HTTP_204_NO_CONTENT)
        </span><span>except</span><span> CustomUser.DoesNotExist:
            </span><span>return</span><span> Response({</span><span>"error"</span><span>: </span><span>"User not found"</span><span>}, status=status.HTTP_404_NOT_FOUND)


</span><span># ✅ User: Manage own profile</span><span>
</span><span>class</span><span></span><span>UserProfileView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsUser]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        serializer = UserSerializer(request.user)
        </span><span>return</span><span> Response(serializer.data)

    </span><span>def</span><span></span><span>put</span><span>(</span><span>self, request</span><span>):
        serializer = UserSerializer(request.user, data=request.data, partial=</span><span>True</span><span>)
        </span><span>if</span><span> serializer.is_valid():
            serializer.save()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"Profile updated"</span><span>, </span><span>"user"</span><span>: serializer.data})
        </span><span>return</span><span> Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
</span></span></code></div></div></pre>

---

## 3️⃣ Update `accounts/urls.py`

<pre class="overflow-visible!" data-start="3311" data-end="4254"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> django.urls </span><span>import</span><span> path
</span><span>from</span><span> .views </span><span>import</span><span> SignupView, AdminUserListView, UserProfileView, AdminOnlyView, StaffOnlyView, UserOnlyView
</span><span>from</span><span> rest_framework_simplejwt.views </span><span>import</span><span> TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(</span><span>"signup/"</span><span>, SignupView.as_view(), name=</span><span>"signup"</span><span>),
    path(</span><span>"login/"</span><span>, TokenObtainPairView.as_view(), name=</span><span>"login"</span><span>),
    path(</span><span>"token/refresh/"</span><span>, TokenRefreshView.as_view(), name=</span><span>"token_refresh"</span><span>),

    </span><span># Role-based endpoints</span><span>
    path(</span><span>"admin-area/"</span><span>, AdminOnlyView.as_view(), name=</span><span>"admin-area"</span><span>),
    path(</span><span>"staff-area/"</span><span>, StaffOnlyView.as_view(), name=</span><span>"staff-area"</span><span>),
    path(</span><span>"user-area/"</span><span>, UserOnlyView.as_view(), name=</span><span>"user-area"</span><span>),

    </span><span># User management</span><span>
    path(</span><span>"admin/users/"</span><span>, AdminUserListView.as_view(), name=</span><span>"admin-users"</span><span>),
    path(</span><span>"admin/users/<int:user_id>/"</span><span>, AdminUserListView.as_view(), name=</span><span>"admin-user-delete"</span><span>),
    path(</span><span>"me/"</span><span>, UserProfileView.as_view(), name=</span><span>"user-profile"</span><span>),
]
</span></span></code></div></div></pre>

---

## 4️⃣ 🔥 Usage Examples

### Signup user

<pre class="overflow-visible!" data-start="4303" data-end="4433"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>POST /signup/
{
  "username": "john",
  "email": "john@example.com",
  "password": "strongpass123",
  "role": "user"
}
</span></code></div></div></pre>

### Login

<pre class="overflow-visible!" data-start="4445" data-end="4525"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>POST /login/
{
  "username": "john",
  "password": "strongpass123"
}
</span></code></div></div></pre>

---

### Admin Actions

#### List all users

<pre class="overflow-visible!" data-start="4570" data-end="4635"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>GET /admin/users/
Authorization: Bearer <admin_token>
</span></code></div></div></pre>

#### Delete a user

<pre class="overflow-visible!" data-start="4656" data-end="4726"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>DELETE /admin/users/3/
Authorization: Bearer <admin_token>
</span></code></div></div></pre>

---

### User Actions

#### Get own profile

<pre class="overflow-visible!" data-start="4771" data-end="4826"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>GET /me/
Authorization: Bearer <user_token>
</span></code></div></div></pre>

#### Update own profile

<pre class="overflow-visible!" data-start="4852" data-end="4944"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>PUT /me/
Authorization: Bearer <user_token>
{
  "email": "newjohn@example.com"
}
</span></code></div></div></pre>

---

✅ Now we have a  **complete role-based user management system** :

* Admin can manage everyone 🔑
* User can only manage themselves 👤
* Staff can have their own restricted endpoints 👷

---

👉 Do you want me to also add **staff permissions** (like “staff can view all users but not delete/update”) to make it even closer to a real company-style system?

##### You said:

yes

###### ChatGPT said:

Alright bro 🚀 let’s add the **Staff role features** so the system feels like a real company’s role hierarchy:

* 👑 **Admin** → full control (create/list/update/delete any user).
* 👷 **Staff** → can **see all users** (read-only), but  **cannot delete/update them** .
* 👤 **User** → can only  **see & update their own profile** .

---

## 1️⃣ Update `accounts/views.py`

We’ll add a new view for  **Staff** .

<pre class="overflow-visible!" data-start="414" data-end="2634"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> rest_framework.views </span><span>import</span><span> APIView
</span><span>from</span><span> rest_framework.response </span><span>import</span><span> Response
</span><span>from</span><span> rest_framework </span><span>import</span><span> status
</span><span>from</span><span> rest_framework.permissions </span><span>import</span><span> IsAuthenticated

</span><span>from</span><span> .serializers </span><span>import</span><span> SignupSerializer, UserSerializer
</span><span>from</span><span> .permissions </span><span>import</span><span> IsAdmin, IsStaff, IsUser
</span><span>from</span><span> .models </span><span>import</span><span> CustomUser


</span><span># ✅ Signup</span><span>
</span><span>class</span><span></span><span>SignupView</span><span>(</span><span>APIView</span><span>):
    </span><span>def</span><span></span><span>post</span><span>(</span><span>self, request</span><span>):
        serializer = SignupSerializer(data=request.data)
        </span><span>if</span><span> serializer.is_valid():
            serializer.save()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"User created successfully"</span><span>}, status=status.HTTP_201_CREATED)
        </span><span>return</span><span> Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


</span><span># ✅ Admin: Full management (list & delete)</span><span>
</span><span>class</span><span></span><span>AdminUserListView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsAdmin]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        users = CustomUser.objects.</span><span>all</span><span>()
        serializer = UserSerializer(users, many=</span><span>True</span><span>)
        </span><span>return</span><span> Response(serializer.data)

    </span><span>def</span><span></span><span>delete</span><span>(</span><span>self, request, user_id</span><span>):
        </span><span>try</span><span>:
            user = CustomUser.objects.get(</span><span>id</span><span>=user_id)
            user.delete()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"User deleted"</span><span>}, status=status.HTTP_204_NO_CONTENT)
        </span><span>except</span><span> CustomUser.DoesNotExist:
            </span><span>return</span><span> Response({</span><span>"error"</span><span>: </span><span>"User not found"</span><span>}, status=status.HTTP_404_NOT_FOUND)


</span><span># ✅ Staff: Read-only access to all users</span><span>
</span><span>class</span><span></span><span>StaffUserListView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsStaff]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        users = CustomUser.objects.</span><span>all</span><span>()
        serializer = UserSerializer(users, many=</span><span>True</span><span>)
        </span><span>return</span><span> Response(serializer.data)


</span><span># ✅ User: Manage own profile</span><span>
</span><span>class</span><span></span><span>UserProfileView</span><span>(</span><span>APIView</span><span>):
    permission_classes = [IsAuthenticated, IsUser]

    </span><span>def</span><span></span><span>get</span><span>(</span><span>self, request</span><span>):
        serializer = UserSerializer(request.user)
        </span><span>return</span><span> Response(serializer.data)

    </span><span>def</span><span></span><span>put</span><span>(</span><span>self, request</span><span>):
        serializer = UserSerializer(request.user, data=request.data, partial=</span><span>True</span><span>)
        </span><span>if</span><span> serializer.is_valid():
            serializer.save()
            </span><span>return</span><span> Response({</span><span>"message"</span><span>: </span><span>"Profile updated"</span><span>, </span><span>"user"</span><span>: serializer.data})
        </span><span>return</span><span> Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
</span></span></code></div></div></pre>

---

## 2️⃣ Update `accounts/urls.py`

Add the  **staff endpoint** :

<pre class="overflow-visible!" data-start="2704" data-end="3779"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> django.urls </span><span>import</span><span> path
</span><span>from</span><span> .views </span><span>import</span><span> (
    SignupView,
    AdminUserListView,
    StaffUserListView,
    UserProfileView,
    AdminOnlyView,
    StaffOnlyView,
    UserOnlyView,
)
</span><span>from</span><span> rest_framework_simplejwt.views </span><span>import</span><span> TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(</span><span>"signup/"</span><span>, SignupView.as_view(), name=</span><span>"signup"</span><span>),
    path(</span><span>"login/"</span><span>, TokenObtainPairView.as_view(), name=</span><span>"login"</span><span>),
    path(</span><span>"token/refresh/"</span><span>, TokenRefreshView.as_view(), name=</span><span>"token_refresh"</span><span>),

    </span><span># Role-based demo endpoints</span><span>
    path(</span><span>"admin-area/"</span><span>, AdminOnlyView.as_view(), name=</span><span>"admin-area"</span><span>),
    path(</span><span>"staff-area/"</span><span>, StaffOnlyView.as_view(), name=</span><span>"staff-area"</span><span>),
    path(</span><span>"user-area/"</span><span>, UserOnlyView.as_view(), name=</span><span>"user-area"</span><span>),

    </span><span># User management</span><span>
    path(</span><span>"admin/users/"</span><span>, AdminUserListView.as_view(), name=</span><span>"admin-users"</span><span>),
    path(</span><span>"admin/users/<int:user_id>/"</span><span>, AdminUserListView.as_view(), name=</span><span>"admin-user-delete"</span><span>),
    path(</span><span>"staff/users/"</span><span>, StaffUserListView.as_view(), name=</span><span>"staff-users"</span><span>),
    path(</span><span>"me/"</span><span>, UserProfileView.as_view(), name=</span><span>"user-profile"</span><span>),
]
</span></span></code></div></div></pre>

---

## 3️⃣ 🔥 Usage Examples

### Staff Actions

#### View all users

<pre class="overflow-visible!" data-start="3850" data-end="3915"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-http"><span>GET /staff/users/
Authorization: Bearer <staff_token>
</span></code></div></div></pre>

Response (example):

<pre class="overflow-visible!" data-start="3936" data-end="4192"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>[</span><span>
  </span><span>{</span><span>"id"</span><span>:</span><span></span><span>1</span><span>,</span><span></span><span>"username"</span><span>:</span><span></span><span>"admin"</span><span>,</span><span></span><span>"email"</span><span>:</span><span></span><span>"admin@example.com"</span><span>,</span><span></span><span>"role"</span><span>:</span><span></span><span>"admin"</span><span>}</span><span>,</span><span>
  </span><span>{</span><span>"id"</span><span>:</span><span></span><span>2</span><span>,</span><span></span><span>"username"</span><span>:</span><span></span><span>"john"</span><span>,</span><span></span><span>"email"</span><span>:</span><span></span><span>"john@example.com"</span><span>,</span><span></span><span>"role"</span><span>:</span><span></span><span>"user"</span><span>}</span><span>,</span><span>
  </span><span>{</span><span>"id"</span><span>:</span><span></span><span>3</span><span>,</span><span></span><span>"username"</span><span>:</span><span></span><span>"staff1"</span><span>,</span><span></span><span>"email"</span><span>:</span><span></span><span>"staff1@example.com"</span><span>,</span><span></span><span>"role"</span><span>:</span><span></span><span>"staff"</span><span>}</span><span>
</span><span>]</span><span>
</span></span></code></div></div></pre>

❌ Staff cannot:

* Delete users (`/admin/users/<id>/`)
* Update other users

---

✅ Now we’ve got  **3 clear roles** :

* **Admin** = 👑 full CRUD over users
* **Staff** = 👷 read-only list of all users
* **User** = 👤 can only manage their own profile
