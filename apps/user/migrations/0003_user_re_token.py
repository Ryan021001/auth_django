# Generated by Django 4.2 on 2023-05-23 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='re_token',
            field=models.CharField(default='', max_length=255),
        ),
    ]
