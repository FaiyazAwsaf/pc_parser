from rest_framework import serializers


class ChatPromptSerializer(serializers.Serializer):
    prompt = serializers.CharField()
