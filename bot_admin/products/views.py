# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
from .models import Product
from django.utils import timezone
import traceback

class ProductCreateView(APIView):
    permission_classes = [HasAPIKey]  # valida automaticamente a chave da API
    authentication_classes = []  # sem autenticação adicional

    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            # Valida campos obrigatórios
            required_fields = ["name", "price", "external_id", "link", "category"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return Response(
                    {"status": "error", "message": f"Campos obrigatórios faltando: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Valida tipos básicos
            try:
                price = float(data.get("price"))
                old_price = float(data.get("old_price")) if data.get("old_price") else None
                discount_percent = float(data.get("discount_percent")) if data.get("discount_percent") else None
                installements = int(data.get("installements")) if data.get("installements") else None
                installements_value = float(data.get("installements_value")) if data.get("installements_value") else None
                interest_free = bool(data.get("interest_free", False))
                
            except (ValueError, TypeError) as e:
                return Response(
                    {"status": "error", "message": f"Erro de tipo nos dados: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Tenta buscar produto existente pelo external_id
            product, created = Product.objects.get_or_create(
                external_id=data.get("external_id"),
                defaults={
                    "name": data.get("name"),
                    "description": data.get("description"),
                    "old_price": old_price,
                    "price": price,
                    "discount_percent": discount_percent,
                    "installements": installements,
                    "installements_value": installements_value,
                    "interest_free": interest_free,
                    "image": data.get("image"),
                    "link": data.get("link"),
                    "category_id": data.get("category"),
                }
            )

            if not created:
                # Produto existe, verificar se algum campo mudou
                fields_to_check = {
                    "name": data.get("name"),
                    "description": data.get("description"),
                    "old_price": old_price,
                    "price": price,
                    "discount_percent": discount_percent,
                    "installements": installements,
                    "installements_value": installements_value,
                    "interest_free": interest_free,
                    "image": data.get("image"),
                    "link": data.get("link"),
                    "category_id": data.get("category"),
                }

                changed = False
                for field, new_value in fields_to_check.items():
                    if getattr(product, field) != new_value:
                        setattr(product, field, new_value)
                        changed = True

                if changed:
                    product.updated_at = timezone.now()
                    product.save()
                    status_msg = "updated"
                else:
                    status_msg = "unchanged"
            else:
                status_msg = "created"

            return Response({"status": status_msg, "received_data": data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(traceback.format_exc())
            return Response(
                {"status": "error", "message": f"Ocorreu um erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )