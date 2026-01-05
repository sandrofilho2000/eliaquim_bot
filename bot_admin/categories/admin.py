from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'created_at', 'updated_at', "active")
    list_editable = ("active",)
    search_fields = ('name', 'description', 'shop')
    readonly_fields = ('created_at', 'updated_at')
