# Generated by Django 4.2.4 on 2023-09-03 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_comment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_name',
            field=models.CharField(default='user', max_length=20),
        ),
    ]