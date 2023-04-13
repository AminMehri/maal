from rest_framework import serializers



class CreateProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    total_price = serializers.IntegerField()
    price = serializers.IntegerField()
    fee_percent = serializers.FloatField()
    description = serializers.CharField(max_length=5000)
    categories = serializers.ListField()
