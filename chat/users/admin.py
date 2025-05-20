from django.contrib import admin
from .models import Message, Chat, MessagesInChat


class MessagesInChatInline(admin.TabularInline):
    model = MessagesInChat
    extra = 2


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("pk", "sender", "timestamp")


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    inlines = (MessagesInChatInline,)
