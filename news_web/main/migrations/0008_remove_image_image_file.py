# Generated by Django 4.2.4 on 2023-09-03 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_image_image_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image_file',
        ),
    ]