# Generated by Django 2.1.7 on 2019-03-24 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0025_profile_user_exp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user_level']},
        ),
    ]
