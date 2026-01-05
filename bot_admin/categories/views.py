from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import generics

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = []
    permission_classes = [HasAPIKey]
    
