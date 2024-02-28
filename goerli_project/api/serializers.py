from rest_framework import serializers

from tokens.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class TokenCreateSerializer(TokenSerializer):
    def create(self, validated_data):
        return Token.objects.create(**validated_data)
