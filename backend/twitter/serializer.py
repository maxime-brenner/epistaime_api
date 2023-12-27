from rest_framework import serializers

class TwitterSerializer(serializers.Serializer):
    datas = serializers.JSONField()