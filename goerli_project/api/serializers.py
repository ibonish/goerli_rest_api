from rest_framework import serializers
from tokens.models import Token


class TokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['media_url', 'owner']

    def create(self, validated_data):
        return Token.objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
