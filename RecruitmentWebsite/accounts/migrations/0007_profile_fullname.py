# Generated by Django 4.1.6 on 2023-06-13 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_email_profile_image_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fullname',
            field=models.CharField(default='Firstname Lastname Here', max_length=255),
        ),
    ]