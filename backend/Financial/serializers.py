from rest_framework import serializers


class WithdrawRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField()