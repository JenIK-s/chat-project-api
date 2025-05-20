from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import Chat, Message, MessagesInChat, User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class MessagesInChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagesInChat
        fields = "__all__"
