# Generated by Django 4.1.6 on 2023-06-18 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fullname',
            field=models.CharField(max_length=255),
        ),
    ]
