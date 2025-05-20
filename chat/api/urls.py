from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, MessageViewSet, ChatViewSet, MessageInChatViewSet

app_name = "api"

router_1 = DefaultRouter()
router_1.register("chat", ChatViewSet)
router_1.register("messages", MessageViewSet)
router_1.register("messages_in_chat", MessageInChatViewSet)
router_1.register("users", UsersViewSet)


urlpatterns = [
    path('', include(router_1.urls)),

]
