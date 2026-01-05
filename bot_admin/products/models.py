from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    installements = models.IntegerField(null=True, blank=True)
    installements_value = models.DecimalField(max_digits=10, decimal_places=4, default=0, null=True, blank=True)
    interest_free = models.BooleanField(default=False)
    image = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=100, unique=True)
    link = models.TextField()
    link_affiliate = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produto"
        ordering = ['-created_at']