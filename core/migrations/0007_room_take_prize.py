# Generated by Django 3.1.5 on 2021-02-06 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_profile_next_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='take_prize',
            field=models.BooleanField(default=False),
        ),
    ]
