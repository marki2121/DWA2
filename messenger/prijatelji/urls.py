from django.urls import path

from prijatelji.views import(
    send_request,
)

app_name = "prijatelji"

urlpatterns = [
    path('friend_request/', send_request, name='friend-request'),
]
