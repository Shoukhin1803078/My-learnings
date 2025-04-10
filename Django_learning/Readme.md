
# Create a virtual environment
python -m venv django_env

# Activate it (Windows)
django_env\Scripts\activate

# Activate it (macOS/Linux)
source django_env/bin/activate

# Install Django
pip install django



# Create a new project
django-admin startproject myproject

# Navigate to the project
cd myproject

# Create an app within your project
python manage.py startapp myapp

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
