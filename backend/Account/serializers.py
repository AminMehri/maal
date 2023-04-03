from rest_framework import serializers



class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SumbitInstaSerializer(serializers.Serializer):
    instagram_id = serializers.CharField(max_length=256)

