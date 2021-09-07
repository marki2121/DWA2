from django.urls import path

from prijatelji.views import(
    send_request,
    lista_zahtijeva_view,
)

app_name = "prijatelji"

urlpatterns = [
    path('friend_request/', send_request, name='friend-request'),
    path('friend_request/<user_id>/', lista_zahtijeva_view, name='friend-requests')
    
]
