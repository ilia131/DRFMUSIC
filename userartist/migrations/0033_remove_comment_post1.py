# Generated by Django 4.2.6 on 2024-03-09 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userartist', '0032_comment_post1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post1',
        ),
    ]
