# Generated by Django 2.1.5 on 2019-02-09 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0006_auto_20190206_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
