# Generated by Django 2.0.2 on 2018-03-23 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaucetTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(db_index=True, max_length=128)),
                ('amount', models.DecimalField(decimal_places=18, max_digits=24)),
                ('transferred_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
