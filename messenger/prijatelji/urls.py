from django.urls import path

from prijatelji.views import(
    send_request,
    lista_zahtijeva_view,
    prihvati,
    odbi,
    cancel,
    ListaPrijateljaView,
)

app_name = "prijatelji"

urlpatterns = [
    #     Lista prijatelja
    path('list/<user_id>', ListaPrijateljaView, name="list"),

    #     Slanje zahtijeva
    path('friend_request/', send_request, name='friend-request'),

    #     Cancel zahtijeva
    path('friend_cancel/', cancel, name='friend-cancel'),
    
    #     Pregled zahtijeva
    path('friend_request/<user_id>/', lista_zahtijeva_view, name='friend-requests'),
    
    #     Prihvacanje zahtijeva
    path('friend_request_accept/<friend_request_id>/', prihvati, name='friend-request-accept'),

    #     Odbijanje zahtijeva
    path('friend_request_denie/<friend_request_id>/', odbi, name='friend-request-denie'),    
]
