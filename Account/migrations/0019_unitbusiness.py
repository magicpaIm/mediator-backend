# Generated by Django 4.0.4 on 2022-06-10 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0018_alter_log_type_alter_remoteaccount_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.businesstype')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.unit')),
            ],
            options={
                'unique_together': {('unit', 'business')},
            },
        ),
    ]
