from django.shortcuts import render


#Pocetna stranica
def pocetna_view(requests, *args, **kwargs):
    context={}
    return render(requests, "main/home.html", context)
