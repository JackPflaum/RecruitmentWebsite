# Generated by Django 4.1.6 on 2023-06-13 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_applied_covering_letter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpositions',
            name='job_summary',
            field=models.TextField(default='Job details to come.'),
        ),
        migrations.AddField(
            model_name='jobpositions',
            name='salary',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='jobpositions',
            name='skills',
            field=models.TextField(blank=True),
        ),
    ]