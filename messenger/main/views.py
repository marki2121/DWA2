from django.shortcuts import render


#Pocetna stranica
def pocetna_view(request, *args, **kwargs):
    context={}

    user = request.user
    
    if user.is_authenticated:
        context['user'] = user

    return render(request, "main/home.html", context)
