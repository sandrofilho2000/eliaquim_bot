from django.db import models

class ShopChoices(models.TextChoices):
    MERCADO_LIVRE = "mercado_livre", "Mercado Livre"

class Category(models.Model):
    name = models.CharField(max_length=100)
    link = models.TextField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shop = models.CharField(
        max_length=50,
        choices=ShopChoices.choices,
        default=ShopChoices.MERCADO_LIVRE
    )
    
    active = models.BooleanField(default=True)
        
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
