# Generated by Django 4.1.6 on 2023-09-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_jobpositions_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpositions',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]