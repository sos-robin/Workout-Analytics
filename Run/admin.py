from django.contrib import admin

# Register your models here.
from .models import Achievement, Profile

admin.site.register(Achievement)
admin.site.register(Profile)