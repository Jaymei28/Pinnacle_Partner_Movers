import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from django.contrib.auth.models import User

def seed_user():
    username = 'testuser'
    password = 'password123'
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email='test@example.com', password=password)
        print(f"Created superuser: {username} with password: {password}")
    else:
        print(f"User {username} already exists.")

if __name__ == '__main__':
    seed_user()
