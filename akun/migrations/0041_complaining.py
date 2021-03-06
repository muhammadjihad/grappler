# Generated by Django 2.1.7 on 2019-03-28 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('akun', '0040_auto_20190328_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('komplain', models.TextField()),
                ('saran', models.TextField()),
                ('receiver_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_complain_user', to=settings.AUTH_USER_MODEL)),
                ('sender_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_complain_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
