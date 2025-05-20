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


class MessageAddSerializer(serializers.ModelSerializer):
    chat = serializers.PrimaryKeyRelatedField(
        queryset=Chat.objects.all(),
        write_only=True
    )

    class Meta:
        model = Message
        fields = ("text", "chat")

    def create(self, validated_data):
        chat = validated_data.pop("chat")
        sender = self.context["request"].user
        message = Message.objects.create(sender=sender, **validated_data)
        MessagesInChat.objects.create(chat=chat, message=message)
        return message


class MessageSerializer(serializers.ModelSerializer):
    sender = UsersSerializer()
    chat = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("pk", "text", "sender", "chat")

    def get_chat(self, obj):
        # Получаем чат из связи через MessagesInChat
        messages_in_chats = obj.chats.all()
        if messages_in_chats.exists():
            return messages_in_chats.first().chat.id
        return None


class MessagesInChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagesInChat
        fields = "__all__"


class ChatReadSerializer(serializers.ModelSerializer):
    participants = UsersSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = '__all__'

    def get_messages(self, obj):
        qs = (
            MessagesInChat.objects
            .filter(chat=obj)
            .select_related('message', 'message__sender')
            .order_by('added_at')
        )
        return MessageSerializer([item.message for item in qs], many=True).data


class ChatCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )

    class Meta:
        model = Chat
        fields = ('name', 'is_group', 'participants')

    def create(self, validated_data):
        participants_id = validated_data.pop("participants")
        chat = Chat.objects.create(**validated_data)
        for participant_id in participants_id:
            chat.participants.add(participant_id)
            chat.save()
        return chat
