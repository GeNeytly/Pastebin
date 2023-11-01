from django.contrib import admin

from posts import models


@admin.register(models.Post)
class UserAdmin(admin.ModelAdmin):
    pass
