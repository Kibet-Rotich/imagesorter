# Generated by Django 5.2.3 on 2025-07-01 10:53

import core.models
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=core.models.image_upload_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('class_names', models.TextField(help_text='Comma-separated class labels')),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LabeledImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('labeled_at', models.DateTimeField(auto_now=True)),
                ('image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='label', to='core.uploadedimage')),
            ],
        ),
        migrations.AddField(
            model_name='uploadedimage',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.uploadsession'),
        ),
    ]
