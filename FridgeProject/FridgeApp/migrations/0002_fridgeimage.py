# Generated by Django 5.1.4 on 2025-01-01 15:10

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FridgeApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FridgeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('alt_text', models.CharField(blank=True, max_length=256, null=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('fridge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='FridgeApp.fridge')),
            ],
            options={
                'verbose_name': 'fridge_image',
                'verbose_name_plural': 'fridge_images',
                'db_table': 'fridge_image',
                'indexes': [models.Index(['date_uploaded'], name='date_uploaded_index')],
            },
        ),
    ]
