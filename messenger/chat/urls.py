from django.urls import path

from chat.views import(
    chat_view,
    poruke,
    SendMessage,
)

app_name = "chat"

urlpatterns = [
    path('', chat_view, name="chat"),
    path("chat/<username>", poruke, name="poruke"),
    path("send/", SendMessage, name="posalji"),
]