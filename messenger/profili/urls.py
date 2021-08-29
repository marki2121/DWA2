from django.urls import path

from profili.views import (
    profil_view,
)

app_name = "account"

urlpatterns = [
    path('<user_id>/', profil_view, name="view"),
]
