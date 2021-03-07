from django.contrib import admin

from . import models


@admin.register(models.ConsentSource)
class ConsentSourceAdmin(admin.ModelAdmin):
    pass
