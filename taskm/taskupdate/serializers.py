from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class loginSerializer(serializers.ModelSerializer):
    """
    Serializer for Login Data
    """
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        else:
            raise serializers.ValidationError({'Msg': 'Invalid Credentials'})