# Generated by Django 2.0.2 on 2018-03-23 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aepp_auth', '0003_auto_20180323_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubuser',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
