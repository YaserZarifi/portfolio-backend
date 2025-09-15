
import os
from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()

    username = os.environ.get('ADMIN_USER')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASS')

    if not all([username, email, password]):
        print("Admin credentials not set in environment variables. Skipping superuser creation.")
        return

    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists.")
        return

    print(f"Creating superuser '{username}'...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully.")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_profile'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
