# Generated by Django 2.1.5 on 2019-02-16 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graplearn', '0007_auto_20190214_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
