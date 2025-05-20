from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Название чата"
    )
    is_group = models.BooleanField(
        default=False,
        verbose_name="Групповой чат"
    )
    participants = models.ManyToManyField(
        User,
        related_name='chats',
        verbose_name="Участники"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return self.name if self.name else f"Чат #{self.id}"


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages_sent',
        verbose_name="Отправитель"
    )
    text = models.TextField(verbose_name="Текст")
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время отправки"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}"


class MessagesInChat(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages_in_chat',
        verbose_name="Чат"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='chats',
        verbose_name="Сообщение"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время добавления в чат"
    )

    class Meta:
        verbose_name = "Сообщение в чате"
        verbose_name_plural = "Сообщения в чатах"
        unique_together = ('chat', 'message')

    def __str__(self):
        return f"Чат {self.chat} | Сообщение {self.message}"