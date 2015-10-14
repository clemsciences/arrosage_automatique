# -*-coding:utf-8-*-
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def accueil(request):
    return render(request, "templates.accueil.html")
    #return HttpResponse("bienvenue")



def parametrage_arrosage(request):
    return HttpResponse("ici on ne paramètre... rien ! haha")

def statistiques_meteorologiques(request):
    return HttpResponse("il fait beau ou pas")

def statistiques_arrosages(request):
    return HttpResponse("pour l'instant on a rien fait, ok?")


def rapport_courriel(request):
    return HttpResponse("ça attendra un petit moment")