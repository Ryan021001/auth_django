# Generated by Django 4.2 on 2023-05-25 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(default='user', max_length=31),
        ),
    ]