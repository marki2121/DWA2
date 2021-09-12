from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include

from profili.views import(
    register_view,
    login_view,
    logout_view,
    search_view,
)

from chat.views import(
    chat_view,
)

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),

    #Login/register forme
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

    #Prijatelji
    path('friend/', include('prijatelji.urls', namespace='friend')),

    # Password reset linkovi (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),

    #Profil
    path('account/', include('profili.urls', namespace='account')),

    #Search

    path('search/', search_view, name="search"),

    #Chat
    path("", include('chat.urls', namespace='poruk')),

]


#pomoc za static filove posto stranica nije objavljena
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
