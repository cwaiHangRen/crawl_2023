# Generated by Django 4.2.4 on 2023-09-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_comment_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_file',
            field=models.ImageField(default='default.jpg', upload_to='images/'),
        ),
    ]
