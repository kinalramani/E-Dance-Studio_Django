# Generated by Django 5.0.7 on 2024-08-03 06:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('f_name', models.CharField(max_length=150)),
                ('l_name', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mob_no', models.CharField(max_length=15)),
                ('bio', models.TextField()),
                ('expertise', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
    ]