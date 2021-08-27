from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profili.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'datum_dolaska', 'zadnji_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id','datum_dolaska', 'zadnji_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
