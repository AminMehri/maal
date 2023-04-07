from rest_framework import serializers


class newDepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()