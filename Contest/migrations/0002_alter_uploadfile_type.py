# Generated by Django 4.0.4 on 2022-06-28 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0029_alter_post_body'),
        ('Contest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resource_business_type', to='Account.businesstype'),
        ),
    ]
