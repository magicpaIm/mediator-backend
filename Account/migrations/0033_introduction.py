# Generated by Django 4.0.4 on 2022-08-24 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0032_alter_comment_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Introduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('detail', models.TextField(null=True)),
                ('type', models.CharField(max_length=255)),
            ],
        ),
    ]
