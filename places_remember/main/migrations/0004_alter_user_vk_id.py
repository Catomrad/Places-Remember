# Generated by Django 5.0.6 on 2024-05-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user_alter_memory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='vk_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
