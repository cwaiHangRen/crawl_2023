# Generated by Django 4.2.4 on 2023-09-03 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_image_image_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image_file',
        ),
        migrations.AddField(
            model_name='image',
            name='image_path',
            field=models.CharField(default='C:\\Users\\86186\\2023Summer\\news_web\\main\\images\\default.jpg', max_length=255),
        ),
    ]
