# Generated by Django 2.1.5 on 2019-02-14 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graplearn', '0005_auto_20190214_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
