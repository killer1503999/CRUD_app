from rest_framework import serializers
from .models import *

class FactoryNameserializers(serializers.ModelSerializer):

    class Meta:
        model=FactoryName
        fields="__all__"

class ProductNameserializers(serializers.ModelSerializer):

    class Meta:
        model=ProductName
        fields="__all__"