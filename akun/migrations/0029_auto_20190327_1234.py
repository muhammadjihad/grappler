# Generated by Django 2.1.7 on 2019-03-27 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0028_auto_20190327_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimoni',
            name='published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
