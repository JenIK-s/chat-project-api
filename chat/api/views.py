from rest_framework.viewsets import ModelViewSet

from .serializers import UserCreateSerializer, UsersSerializer, MessageSerializer, ChatSerializer, MessagesInChatSerializer
from users.models import Chat, Message, MessagesInChat, User


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageInChatViewSet(ModelViewSet):
    queryset = MessagesInChat.objects.all()
    serializer_class = MessagesInChatSerializer
