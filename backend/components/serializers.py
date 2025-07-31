from rest_framework import serializers
from .models import ComponentCategory, Component


class ComponentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentCategory
        fields = ["id", "name", "image_url"]


class ComponentSerializer(serializers.ModelSerializer):
    category = ComponentCategorySerializer()

    class Meta:
        model = Component
        fields = ["id", "category", "name", "brand", "model", "specs"]
