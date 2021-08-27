from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from profili.forms import RegistreationForm, LoginForm

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

