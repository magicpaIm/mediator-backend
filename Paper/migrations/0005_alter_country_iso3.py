# Generated by Django 4.0.3 on 2022-03-24 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0004_country_rename_review_reviewtype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='iso3',
            field=models.CharField(max_length=3, null=True),
        ),
    ]