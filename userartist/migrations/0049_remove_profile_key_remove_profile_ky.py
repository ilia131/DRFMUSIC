# Generated by Django 4.2.6 on 2024-03-10 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userartist', '0048_alter_profile_key_alter_profile_ky'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='key',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ky',
        ),
    ]
