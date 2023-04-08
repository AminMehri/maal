from rest_framework import serializers


class CreateConversationSerializer(serializers.Serializer):
    subject = serializers.CharField(max=256)
    text = serializers.CharField(max=2048)

    
class AddTicketSerializer(serializers.Serializer):
    text = serializers.CharField(max=2048)
    conversationId = serializers.IntegerField()


