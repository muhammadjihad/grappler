# Generated by Django 2.1.5 on 2019-02-10 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0010_profile_koin'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('Reguler', 'Reguler'), ('Premium', 'Premium')], default='Reguler', max_length=25),
            preserve_default=False,
        ),
    ]
