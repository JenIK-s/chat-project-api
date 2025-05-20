from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import UsersSerializer, MessageAddSerializer, MessageSerializer, ChatReadSerializer, MessagesInChatSerializer, ChatCreateSerializer
from users.models import Chat, Message, MessagesInChat, User


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return MessageAddSerializer
        return MessageSerializer


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        # на действиях create/update — пишущий, иначе — читающий
        if self.action in ('create', 'update', 'partial_update'):
            return ChatCreateSerializer
        return ChatReadSerializer

    def perform_create(self, serializer):
        chat = serializer.save()
        # автор автоматически добавляется, если его нет в списке
        if self.request.user not in chat.participants.all():
            chat.participants.add(self.request.user)


class MessageInChatViewSet(ModelViewSet):
    queryset = MessagesInChat.objects.all()
    serializer_class = MessagesInChatSerializer
    permission_classes = (IsAuthenticated,)
