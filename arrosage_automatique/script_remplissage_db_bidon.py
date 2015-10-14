# -*-coding:utf-8-*-
__author__ = 'Clément'

from datetime import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrosage_automatique.settings")
from gestion_arrosage_automatique.models import *



Arrosage(duree=601).save()

ConditionsMeteorologiques(temperature=25.0, humidite_relative=45.3).save()

ConditionArrosage(temperature_min=20, humidite_max=80,frequence_min=1, heure_min=21, heure_max=23, duree=600).save()