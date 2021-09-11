from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max

from chat.models import Poruke
from profili.models import Account

def SendMessage(request):
    user = request.user

    if user.is_authenticated and request.method == 'POST':
        to_user_username = request.POST.get('to_user')

        if to_user_username:
            body = request.POST.get('body')

            if body:
                to_user = Account.objects.get(username=to_user_username)
                Poruke.send_message(od_user=user, za_user=to_user, body=body)
                return redirect('poruk:poruke', username=to_user_username)
            else:
                return HttpResponse("No message")
        else:
            return HttpResponse("No return adress")
    else:
        return redirect('login')

def chat_view(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        messages = Poruke.get_message(user=request.user)
        active_direct = None
        directs = None

        if messages:
            message = messages[0]
            active_direct = message['user'].username
            directs = Poruke.objects.filter(user=request.user, za_user=message['user'])
            directs.update(is_read=True)
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

def poruke(request, username):
    user = request.user
    context = {}
    if user.is_authenticated:
        messages = Poruke.get_message(user=user)
        active_direct = username
        directs = Poruke.objects.filter(user=user, za_user__username=username)
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == username:
                message['unread'] = 0

        context = {
            'poruke': directs,
            'messages': messages,
            'active_direct': active_direct,
            }
    else:
        redirect("login")

    return render(request, 'main/home.html', context)

