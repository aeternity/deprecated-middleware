# Generated by Django 2.0.2 on 2018-03-12 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epoch_extra', '0003_auto_20180312_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aename',
            name='claim_salt',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
