from django.contrib import admin
from example_api.models import ExampleApi

@admin.register(ExampleApi)

class ExampleApiAdmin(admin.ModelAdmin):
    list_display=("name",)
