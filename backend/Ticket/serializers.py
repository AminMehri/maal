from rest_framework import serializers


class CreateTicketSerializer(serializers.Serializer):
    subject = serializers.CharField()
    description = serializers.CharField()
