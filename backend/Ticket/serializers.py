from rest_framework import serializers


class CreateConversationSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=256)
    text = serializers.CharField(max_length=2048)

    
class AddTicketSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2048)
    conversationId = serializers.IntegerField()