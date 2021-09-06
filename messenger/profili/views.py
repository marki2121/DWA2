from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from profili.forms import RegistreationForm, LoginForm
from profili.models import Account

def register_view(requests, *args, **kwargs):
    user = requests.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}")
    

    context = {}

    if requests.POST:
        form = RegistreationForm(requests.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(requests, account)
            destinacija = kwargs.get('next')
            if destinacija:
                return redirect(destinacija)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistreationForm()
        context['registration_form'] = form
    
    return render(requests, 'profili/register.html', context)

def login_view(requests, *args, **kwargs):
    context = {}

    user = requests.user
    if user.is_authenticated:
        return redirect('home')
    
    if requests.POST:
        form = LoginForm(requests.POST)
        if form.is_valid():
            email = requests.POST['email']
            password = requests.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(requests, user)
                return redirect('home')
    else:
        form = LoginForm()

    context['login_form'] = form

    return render(requests, 'profili/login.html', context)
    

def logout_view(request):
	logout(request)
	return redirect("home")

def profil_view(request, *args, **kwargs):
    context = {}

    user_id = kwargs.get("user_id")

    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Na ovo nismo bili spremni.")

    if account:
        context['id'] = account.id
        context['email'] = account.email
        context['username'] = account.username
        context['profile_image'] = account.profile_image.url
        
        #variable za tamplate
        is_self = True
        is_friend = False
        user = request.user

        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request, "profili/profil.html", context)

def search_view(request, *args, **kwargs):
    context = {}

    if request.method == 'GET':
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            rezultati = Account.objects.filter(username__icontains=search_query).distinct()
            
            user = request.user
            accounts = []

            for account in rezultati:
                accounts.append((account, False)) # dok ne napravim frendove !!!
            
            context['accounts'] = accounts

    return render(request, "profili/search.html", context)


        

