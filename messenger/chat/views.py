from django.shortcuts import render, redirect
from django.http import HttpResponse

from chat.models import Poruke
from profili.models import Account


# Slanje poruke
def SendMessage(request):
    user = request.user

    # Provjera autentikacije i metode
    if user.is_authenticated and request.method == 'POST':
        to_user_username = request.POST.get('to_user')

        # User kojem saljemo
        if to_user_username:
            body = request.POST.get('body')

            if body:
                #Slanje poruke
                to_user = Account.objects.get(username=to_user_username)
                Poruke.send_message(od_user=user, za_user=to_user, body=body)
                return redirect('poruk:poruke', username=to_user_username)
            else:
                return HttpResponse("No message")
        else:
            return HttpResponse("No return adress")
    else:
        return redirect('login')

# Chat view
def chat_view(request):
    user = request.user
    context = {}
    #Provjera autentikacije
    if user.is_authenticated:
        messages = Poruke.get_message(user=request.user) #Dohvacanje poruka
        active_direct = None
        directs = None

        if messages:
            # Postavljanje varijabli
            message = messages[0]
            active_direct = message['user'].username
            directs = Poruke.objects.filter(user=request.user, za_user=message['user'])
            for message in messages:
                if message['user'].username == active_direct:
                    message['unread'] = 0

        context = {
            'directs': directs,
            'messages': messages,
            'active_direct': active_direct,
            }
    else:
        redirect("login")

    return render(request, 'main/home.html', context)

# View za izlistavanje poruka s userom
def poruke(request, username):
    user = request.user
    context = {}

    # Provjera autentikacija
    if user.is_authenticated:
        messages = Poruke.get_message(user=user)
        active_direct = username
        #Dohvacanje poruka s userom 
        directs = Poruke.objects.filter(user=user, za_user__username=username)
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == username:
                # Postavljamo da su poruke procitane
                message['unread'] = 0

        context = {
            'poruke': directs,
            'messages': messages,
            'active_direct': active_direct,
            }
    else:
        redirect("login")

    return render(request, 'main/home.html', context)

