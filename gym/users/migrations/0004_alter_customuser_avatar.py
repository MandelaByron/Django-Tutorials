# Generated by Django 5.1.1 on 2024-09-29 09:36

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to=users.models.get_random_filename),
        ),
    ]
