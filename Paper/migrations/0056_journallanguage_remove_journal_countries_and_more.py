# Generated by Django 4.0.4 on 2022-08-04 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Paper', '0055_language_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='journal',
            name='countries',
        ),
        migrations.AddField(
            model_name='journal',
            name='languages',
            field=models.ManyToManyField(blank=True, through='Paper.JournalLanguage', to='Paper.language'),
        ),
        migrations.DeleteModel(
            name='JournalCountry',
        ),
        migrations.AddField(
            model_name='journallanguage',
            name='journal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_country', to='Paper.journal'),
        ),
        migrations.AddField(
            model_name='journallanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_language', to='Paper.language'),
        ),
    ]