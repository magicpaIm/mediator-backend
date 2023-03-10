# Generated by Django 4.0.3 on 2022-04-27 01:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0016_delete_upload'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Paper', '0032_alter_author_country_alter_author_submit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_type', to='Account.businesstype'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='submit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submit_upload_file', to='Paper.submit'),
        ),
    ]
