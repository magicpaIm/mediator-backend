# Generated by Django 4.0.3 on 2022-04-21 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0028_uploadfile_submit'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='uploadfile',
            unique_together={('requirement', 'submit')},
        ),
    ]
