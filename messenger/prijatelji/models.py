from django.db import models
from django.utils import timezone
from django.conf import settings 

#Model za listu prijatelja
class ListaPrijatelja(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="user")
    prijatelji = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="prijatelji")

    def __str__(self):
        return self.user.username

    def add_friend(self, account): #Dodavanje prijatelja
        if not account in self.prijatelji.all():
            self.prijatelji.add(account)
            self.save()    

    def remove_friend(self, account): #Brisanje prijatelja
        if account in self.prijatelji.all():
            self.prijatelji.remove(account)
            self.save()

    def unfriend(self, removee): #kako postati neprijatelji
        remover_fl = self

        remover_fl.remove_friend(removee)

        friends_list = ListaPrijatelja.objects.get(user=removee)
        friends_list.remove_friend(remover_fl.user)

    def is_friend(self, prijatelj): # provjera prijateljstva

        if prijatelj in self.prijatelji.all():
            return True
        else:
            return False

class ZahtijevPrijateljstva(models.Model):

    posiljatelj = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="sender")
    primatelj = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reciver")

    is_active = models.BooleanField(blank=False, null=False, default=True)

    vrijeme = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.posiljatelj.username

    def prihvaceno(self): # updatati fl od oba usera
        primatelj_fl = ListaPrijatelja.objects.get(user = self.primatelj)

        if primatelj_fl:
            primatelj_fl.add_friend(self.posiljatelj)
            posiljatelj_fl = ListaPrijatelja.objects.get(user = self.posiljatelj)
            if posiljatelj_fl:
                posiljatelj_fl.add_friend(self.primatelj)
                self.is_active = False
                self.save()

    def odbijeno(self): #odbijanje zahtijeva
        self.is_active = False
        self.save()

    def otkazano(self): #cancel zahtijeva od strane posiljatelja
        self.is_active = False
        self.save()

    






        