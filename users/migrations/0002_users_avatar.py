# Generated by Django 5.1.3 on 2024-11-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to='profile-portraits'),
        ),
    ]
