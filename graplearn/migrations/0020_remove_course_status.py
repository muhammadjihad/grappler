# Generated by Django 2.1.5 on 2019-02-22 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graplearn', '0019_auto_20190221_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='status',
        ),
    ]
