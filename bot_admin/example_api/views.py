# example_api/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from example_api.models import ExampleApi
from example_api.serializers import ExampleApiSerializer

class ExampleApiListView(generics.ListAPIView):
    queryset = ExampleApi.objects.all()
    serializer_class = ExampleApiSerializer
    permission_classes = [AllowAny] 

class ExampleApiDetailView(generics.RetrieveAPIView):
    queryset = ExampleApi.objects.all()
    serializer_class = ExampleApiSerializer
    lookup_field = 'id' 
    permission_classes = [AllowAny]
