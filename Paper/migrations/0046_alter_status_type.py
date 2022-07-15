# Generated by Django 4.0.4 on 2022-07-20 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0045_resource_flag_status_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='type',
            field=models.CharField(choices=[('submission', 'Submission'), ('request', 'Request'), ('resource upload', 'Resource Upload')], default='submission', max_length=64),
        ),
    ]