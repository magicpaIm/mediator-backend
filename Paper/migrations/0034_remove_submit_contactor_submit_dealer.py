# Generated by Django 4.0.3 on 2022-04-27 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Paper', '0033_alter_order_type_alter_order_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submit',
            name='contactor',
        ),
        migrations.AddField(
            model_name='submit',
            name='dealer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='submit_dealer', to=settings.AUTH_USER_MODEL),
        ),
    ]
