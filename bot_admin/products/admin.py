from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'name',
        'shop_name',
        'old_price',
        'price',
        'discount_percent',
        'installements',
        'installements_value',
        'interest_free',
        'created_at',
        'updated_at',
    )

    list_display_links = ('image_preview', 'name')
    search_fields = ('name', 'description', 'external_id')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def shop_name(self, obj):
        if obj.category:
            return obj.category.get_shop_display()
        return '-'
    shop_name.short_description = 'Loja'

    def image_preview(self, obj):
        image_url = obj.image or 'https://ciampa-illustration.com/wp-content/uploads/woocommerce-placeholder.png'

        return format_html(
            '<img src="{}" style="width:100px;height:100px;border-radius:50%;object-fit:cover;" />',
            image_url
        )
    image_preview.short_description = 'Imagem'
