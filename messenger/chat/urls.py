from django.urls import path

from chat.views import(
    chat_view,
    poruke,
    SendMessage,
)

app_name = "chat"

urlpatterns = [
    # Pocetni chat view
    path('', chat_view, name="chat"),
    
    # Ocitavanje cheta s userom
    path("chat/<username>", poruke, name="poruke"),
    
    # Slanje poruka
    path("send/", SendMessage, name="posalji"),
]