# Generated by Django 4.0.3 on 2022-04-21 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0029_alter_uploadfile_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='submit_status', to='Paper.status'),
        ),
    ]
