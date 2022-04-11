# Generated by Django 3.1.2 on 2022-04-08 14:45

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='', storage=gdstorage.storage.GoogleDriveStorage(), upload_to='profile_img/'),
        ),
    ]
