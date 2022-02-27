from django.contrib import admin
from .models import Advertisement, Category, Location


@admin.register(Advertisement, Category, Location)
class AdsAdmin(admin.ModelAdmin):
    pass
