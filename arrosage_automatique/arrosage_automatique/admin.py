# -*-coding:utf-8-*-
__author__ = 'Clément'

from django.contrib import admin
from gestion_arrosage_automatique.models import *


admin.site.register(ConditionArrosage)
admin.site.register(Arrosage)
admin.site.register(ConditionsMeteorologiques)
admin.site.register(Courriel)