# Generated by Django 5.0.6 on 2024-05-28 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Run', '0004_achievement_user_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(default=1, upload_to='img'),
        ),
    ]
