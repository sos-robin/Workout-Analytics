from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    distance_covered = models.DecimalField(max_digits=5, decimal_places=2)
    time_hours = models.PositiveIntegerField()
    time_minutes = models.PositiveIntegerField()
    time_seconds = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    average_speed = models.DecimalField(max_digits=5, decimal_places=2)
    achievement_date = models.DateField()
    achievement_photo = models.ImageField(upload_to='img')
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.achievement_date)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Achievement on {self.achievement_date}"

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_photo = models.ImageField(upload_to='img', default='img/default_profile.png')


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
