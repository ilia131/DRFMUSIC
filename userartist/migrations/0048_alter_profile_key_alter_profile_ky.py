# Generated by Django 4.2.6 on 2024-03-10 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userartist', '0047_alter_profile_key_alter_profile_ky'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='key',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ky',
            field=models.SlugField(null=True),
        ),
    ]
