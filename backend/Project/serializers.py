from rest_framework import serializers



class CreateProjectSerializer(serializers.Serializer):
    title = serializers.CharField()
    total_price = serializers.IntegerField()
    price = serializers.IntegerField()
    fee_percent = serializers.FloatField()
    description = serializers.CharField()
    categories = serializers.ListField()
    files = serializers.FileField()