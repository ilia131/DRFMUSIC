# Generated by Django 4.2.6 on 2024-03-04 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userartist', '0016_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
