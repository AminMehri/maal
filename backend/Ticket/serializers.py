from rest_framework import serializers


class CreateTicketSerializer(serializers.Serializer):
    subject = serializers.CharField(max=256)
    text = serializers.CharField(max=2048)
