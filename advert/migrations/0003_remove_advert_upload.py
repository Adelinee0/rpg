# Generated by Django 4.2.2 on 2023-06-30 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0002_alter_advert_upload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advert',
            name='upload',
        ),
    ]
