# Generated by Django 5.1.1 on 2024-09-29 09:36

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blog_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-updated', '-publish']},
        ),
        migrations.AddField(
            model_name='blog',
            name='thumbnail',
            field=models.ImageField(default='default_thumbnail.jpg', upload_to=blog.models.get_random_filename),
        ),
    ]
