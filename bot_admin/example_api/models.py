from core.models import BaseModel
from django.db import models

class ExampleApi(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nome")

    class Meta:
        verbose_name = "Exemplo"

    def __str__(self):
        return self.name