from django.contrib import admin

from . import models


@admin.register(models.SupplyPoint)
class SupplyPointAdmin(admin.ModelAdmin):
    list_display = ["identifier"]


@admin.register(models.Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ["read_at", "value"]
