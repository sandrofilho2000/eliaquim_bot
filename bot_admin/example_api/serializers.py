from rest_framework import serializers
from example_api.models import ExampleApi

class ExampleApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleApi
        fields = "__all__"