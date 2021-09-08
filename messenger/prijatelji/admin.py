from django.contrib import admin
from prijatelji.models import ListaPrijatelja, ZahtijevPrijateljstva


#Dodavanje liste prijatelja na admin site
class ListaPrijateljaAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields  = ['user']
    readonly_fields  = ['user']

    class Meta:
        model = ListaPrijatelja

admin.site.register(ListaPrijatelja, ListaPrijateljaAdmin)

#Dodavanje zahtijeva na admin site
class ZahtijevPrijateljstvaAdmin(admin.ModelAdmin):
    list_filter = ['posiljatelj', 'primatelj']
    list_display = ['posiljatelj', 'primatelj']
    search_fields  = ['posiljatelj__username', 'primatelj__username']

    class Meta:
        model = ZahtijevPrijateljstva

admin.site.register(ZahtijevPrijateljstva, ZahtijevPrijateljstvaAdmin)
