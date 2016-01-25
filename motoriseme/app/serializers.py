from app.models import Rider
from django.contrib.auth.models import User
from rest_framework import serializers


class RiderSerializer(serializers.Serializer):
    user = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    nickname = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    def create(self, rider):
        return Rider.objects.create(**rider)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('username', instance.user)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance