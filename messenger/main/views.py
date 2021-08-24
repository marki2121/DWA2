from django.shortcuts import render

def pocetna_view(requests, *args, **kwargs):
    context={}
    return render(requests, "main/home.html", context)
