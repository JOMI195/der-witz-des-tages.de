# Generated by Django 5.0.7 on 2024-08-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_core', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
