from django.db import models
from django.conf import settings 
from django.db.models import Max

from profili.models import Account

class Poruke(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="user_msg")
    od_user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="od_user")
    za_user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="za_user")

    body = models.TextField(max_length=10000, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    #Slanje poruka 
    def send_message(od_user, za_user, body):
        sender_msg = Poruke(
            user = od_user,
            od_user = od_user,
            za_user = za_user,
            body = body,
            is_read = True
        )
        sender_msg.save()

        reciver_msg = Poruke(
            user = za_user,
            od_user = od_user,
            za_user = od_user,
            body = body,
        )
        reciver_msg.save()

        return sender_msg

    #Ocitavanje poruka 
    def get_message(user):
        #Dohvacanje poredano od najnovije do najsatarije poruke
        messages = Poruke.objects.filter(user=user).values('za_user').annotate(last=Max('date')).order_by('-last')
        users = []
        for message in messages:
            users.append({
                'user': Account.objects.get(pk=message['za_user']), #User poruke
                'last': message['last'], # Zadnja poruka
                'unread': Poruke.objects.filter(user=user, za_user__pk=message['za_user'], is_read=False).count() # Dali je poruka procitana
                })
        return users




