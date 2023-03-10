# Generated by Django 4.0.3 on 2022-03-23 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0002_article_requirement_resource_status_submit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='status_logs',
            field=models.ManyToManyField(blank=True, through='Paper.OrderStatusLog', to='Paper.status'),
        ),
        migrations.AddField(
            model_name='resource',
            name='is_download',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='orderstatuslog',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Paper.order'),
        ),
        migrations.AddField(
            model_name='orderstatuslog',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Paper.status'),
        ),
    ]
