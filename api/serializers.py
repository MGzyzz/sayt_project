from rest_framework import serializers
from accounts.models import User
from orandevu.models.message import Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'description', 'status', 'email', 'image']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'sender_name', 'receiver', 'text', 'timestamp']

