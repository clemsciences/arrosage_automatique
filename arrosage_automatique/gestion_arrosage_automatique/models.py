# -*-coding:utf-8-*-
from django.db import models

class ConditionArrosage(models.Model):
    #compteur = models.PositiveIntegerField(primary_key = True)
    temperature_min = models.FloatField()
    humidite_max = models.FloatField()
    frequence_min = models.SmallIntegerField()
    heure_min = models.IntegerField()
    heure_max = models.IntegerField()
    duree = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    #[compteur, temperature_min, humidite_max, frequence_min, heure_min, heure_max ]



class Arrosage(models.Model):
    #compteur = models.PositiveIntegerField(primary_key=True)
    duree = models.FloatField()
    date_exacte = models.DateTimeField(auto_now_add=True)
class Courriel(models.Model):
    #compteur = models.PositiveIntegerField(primary_key=True)
    emetteur = models.EmailField()
    recepteur = models.EmailField()
    objet = models.CharField(max_length=50)
    texte = models.TextField()
    date_exacte = models.DateTimeField(auto_now_add=True)

class ConditionsMeteorologiques(models.Model):
    #compteur = models.PositiveIntegerField(primary_key= True)
    temperature = models.FloatField()
    humidite_relative = models.FloatField()
    date_exacte = models.DateTimeField(auto_now_add=True)
    #pression_atmospherique = models.IntegerField()
    #pluie = models.IntegerField()