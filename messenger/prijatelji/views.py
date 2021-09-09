from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from profili.models import Account
from prijatelji.models import ZahtijevPrijateljstva, ListaPrijatelja

def send_request(request):
    user = request.user #Ddohvacamo trenutnog usera

    payload = {}

    if request.method == "POST" and user.is_authenticated: #Ako je metoda zahtijeva POST i user je prijavljeni
        user_id = request.POST.get("receiver_user_id") # Dohvacamo id osobe kojoj se zahtijev salje

        if user_id: #Ako ga dohvatimo
            primatelj = Account.objects.get(pk=user_id) #Dohvacamo njegov primarni kljuc
            try:
                friend_requests = ZahtijevPrijateljstva.objects.filter(posiljatelj=user, primatelj=primatelj) #Dohvacamo listu zahtijeva

                try:
                    for request in friend_requests: # loopamo kroz sve zahtijeve
                        if request.is_active: # ako je vec poslan
                            raise Exception("You already sent them a friend request.")
                    
                    friend_request = ZahtijevPrijateljstva(posiljatelj=user ,primatelj=primatelj, is_active=True) # saljemo zahtijev
                    friend_request.save() # spremamo ga 
                    payload['response'] = "Friend request sent."

                except Exception as e:
                    payload['response'] = str(e) # u slucaju errora
            except ZahtijevPrijateljstva.DoesNotExist: # ako osoba nema listu zahtijeva stvaramo novu
                friend_request = ZahtijevPrijateljstva(posiljatelj=user, primatelj=primatelj, is_active=True)
                friend_request.save()
                payload['response'] = "Friend request sent."
        
            if payload['response'] == None:
                payload['response'] = "Something went wrong." # error
        else:
            payload['response'] = "Unable to sent a friend request." # error
    else:
        payload['response'] = "You must be authenticated to send a friend request." # ako nismo prijavljeni 
    return HttpResponse(json.dumps(payload), content_type="application/json") # slanje payloada

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

    #Renderw
    return render(request, "prijatelji/lista_zahtijeva.html", context)

# Prihvacanje zahtijeva
def prihvati(request, *args, **kwargs):
    user = request.user # ddohvacamo usera na stranici 

    payload = {}

    if request.method == 'GET' and user.is_authenticated: # provjera metode i prijave 
        frend_requests_id = kwargs.get('friend_request_id') # Dohvacamo id 

        if frend_requests_id: # ako id dohvatimo 
            friend_request = ZahtijevPrijateljstva.objects.get(pk = frend_requests_id) # dohvacamo kljuc

            if friend_request.primatelj == user: # ako je user primatelj zahtijeva
                if friend_request:
                    friend_request.prihvaceno() # zahtijev prihavtimo 
                    payload['response'] = "Friend request accepted."
# ERRORI                
                else:
                    payload['response'] = "Ups."
            else:
                 payload['response'] = "Nemas sta acceptat."
        else:
             payload['response'] = "to nije tvoje da prihvacas."

    else:
        payload['response'] = "Login plizz"

    #Slanje payloada
    return HttpResponse(json.dumps(payload), content_type="application/json")

#Odbijanje zahtijeva
def odbi(request, *args, **kwargs):
    user = request.user # Dohvacanje usera

    payload = {}

    if request.method == 'GET' and user.is_authenticated: # provjera autentikacije i metode 
        frend_requests_id = kwargs.get('friend_request_id') # dohvacanje id-a

        if frend_requests_id:
            frend_request = ZahtijevPrijateljstva.objects.get(pk = frend_requests_id) # dohvacanje zahtijeva

            if frend_request.primatelj == user: # provijera dali je zahtijev nas
                if frend_request:
                    frend_request.odbijeno() # dobijanje
                    payload['response'] = "Friend request denied."
# ERRORI
                else:
                    payload['response'] = "Ups."
            else:
                payload['response'] = "Nemas sta odbit"
        else:
            payload['response'] = "To nije tvoje da odbijas"
    else:
        payload['response'] = "Login plizz"
    
    return HttpResponse(json.dumps(payload), content_type="application/json")

def cancel(request, *args, **kwargs):
    user = request.user

    payload = {}

    if request.method == "POST" and user.is_authenticated: 
        user_id = request.POST.get("receiver_user_id")

        if user_id:
            account = Account.objects.get(pk=user_id)

            try:
                f_requests = ZahtijevPrijateljstva.objects.filter(posiljatelj=user, primatelj=account, is_active=True)
            
            except f_requests.DoesNotExist:
                return HttpResponse("Nothing to get canceled.")

            if len(f_requests) > 1:
                for request in f_requests:
                    request.otkazano()
                payload['response'] = "Friend request canceled."
            else:
                f_requests.first().otkazano()
                payload['response'] = "Friend request canceled."
        else:
            payload['response'] = "User DoesNotExist"
    else:
        payload['response'] = "Login plizz"
    
    return HttpResponse(json.dumps(payload), content_type='application/json')


def ListaPrijateljaView(request, *args, **kwargs):
    user = request.user

    context = {}

    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        
        if user_id:
            try:
                Ouser = Account.objects.get(pk=user_id)
            except:
                return HttpResponse("User is dead.")
            try:
                f_list = ListaPrijatelja.objects.get(user=Ouser)
            except:
                return HttpResponse('You have no friends?!')
            
            #Moras biti frend da bi vidia frend listu
            if user != Ouser:
                if not user in f_list.prijatelji.all():
                    return HttpResponse("You need to be his/her friend you creep")
            
            prijatelji = []

            auth_user_fl = ListaPrijatelja.objects.get(user=user)
            for friend in f_list.prijatelji.all():
                prijatelji.append((friend, auth_user_fl.is_friend(friend)))
            
            context['lista_prijatelja'] = prijatelji
    else:
        return HttpResponse("You need to be his/her friend you creep")
    return render(request, 'prijatelji/lista_prijatelja.html', context)



                    
