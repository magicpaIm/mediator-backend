# Generated by Django 4.0.3 on 2022-04-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0013_alter_country_iso_alter_country_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='phone_code',
            field=models.SmallIntegerField(null=True),
        ),
    ]
