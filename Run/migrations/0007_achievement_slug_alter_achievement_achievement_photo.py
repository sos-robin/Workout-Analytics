# Generated by Django 5.0.6 on 2024-05-31 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Run', '0006_alter_profile_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='achievement_photo',
            field=models.ImageField(upload_to='img'),
        ),
    ]
