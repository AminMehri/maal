from rest_framework import serializers


class newDepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min=10000, max=100000000)
