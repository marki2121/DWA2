from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from profili.models import Account
from prijatelji.models import ZahtijevPrijateljstva

def send_request(request):
    user = request.user

    payload = {}

    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")

        if user_id:
            primatelj = Account.objects.get(pk=user_id)
            try:
                friend_requests = ZahtijevPrijateljstva.objects.filter(posiljatelj=user, primatelj=primatelj)

                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request.")
                    
                    friend_request = ZahtijevPrijateljstva(posiljatelj=user ,primatelj=primatelj, is_active=True)
                    friend_request.save()
                    payload['response'] = "Friend request sent."

                except Exception as e:
                    payload['response'] = str(e)
            except ZahtijevPrijateljstva.DoesNotExist:
                friend_request = ZahtijevPrijateljstva(posiljatelj=user, primatelj=primatelj, is_active=True)
                friend_request.save()
                payload['response'] = "Friend request sent."
        
            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to sent a friend request."
    else:
        payload['response'] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")

def lista_zahtijeva_view(request, *args, **kwargs):
    #pregled liste zahtijeva
    context = {}

    user = request.user
    #provjera dali je user autenticiran
    if user.is_authenticated:
        #Dohvacanje pk userna koi pristupa stranici
        user_id = kwargs.get("user_id")
        account = Account.objects.get(pk=user_id)

        #Provjera dali smo na svome profilu
        if account == user:
            frend_requests = ZahtijevPrijateljstva.objects.filter(primatelj=account, is_active=True)
            context['friend_requests'] = frend_requests

        #Ako smo na tuđoj stranici
        else:
            return HttpResponse("Ooooooo nononono not your page!!!")
    
    #Ako nije prijavljen redirect login
    else:
        redirect("login")

    #Render
    return render(request, "prijatelji/lista_zahtijeva.html", context)



                    
