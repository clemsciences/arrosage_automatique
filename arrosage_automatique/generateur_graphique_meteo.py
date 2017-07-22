# -*-coding:utf-8-*-
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os

from constantes import *

__author__ = 'besnier'

conversion_mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre",
                       "novembre", "decembre"]

conversion_jour = {"Mon" : "Lundi", "Tue" : "Mardi", "Wed" : "Mercredi", "Thu" : "Jeudi", "Fri" : "Vendredi",
                       "Sat" : "Samedi", "Sun" : "Dimanche"}

nombre_jour_par_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def obtenir_courbe_temperature_jour(temps, temperatures):
    # jour en datetime.datetime.now()
    jour = temps[0]
    jour_semaine = jour.ctime()[:3]
    nf_min = MITJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
    nom_minima_temperature = os.path.join(DIRECTORY_IMAGES, nf_min)
    #nom_minima_temperature = "minima_temperature_jour.png"
    temps_minima_par_heure = list(set([timme.hour for timme in temps]))
    temps_minima_par_heure.sort()
    minima_par_heure = [min([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure]) for heure in temps_minima_par_heure]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(temps_minima_par_heure, minima_par_heure, marker="*")
    plt.savefig(nom_minima_temperature)
    plt.close()

    nf_max = MATJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
    nom_maxima_temperature = os.path.join(DIRECTORY_IMAGES, nf_max)
    #nom_maxima_temperature = "maxima_temperature_jour.png"
    temps_maxima_par_heure = list(set([timme.hour for timme in temps]))
    temps_maxima_par_heure.sort()
    maxima_par_heure = [max([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure and type(tempe) == float] ) for heure in temps_maxima_par_heure]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(temps_maxima_par_heure, maxima_par_heure, marker="*")
    plt.savefig(nom_maxima_temperature)
    plt.close()

    nf_moy = MOTJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
    nom_moyennes_temperatures = os.path.join(DIRECTORY_IMAGES, nf_moy)
    #nom_moyennes_temperatures = "moyennes_temperature_jour.png"
    temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
    temps_moyennes_par_heure.sort()
    moyennes_par_heure = [np.mean([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure and type(tempe) == float]) for heure in temps_moyennes_par_heure]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
    plt.savefig(nom_moyennes_temperatures)
    plt.close()
    #return nf_min, nf_max, nf_moy


def obtenir_courbe_temperature_mois(temps, temperatures, annee, mois):
    # jour en datetime.datetime.now()    
    jours = list(set([jour.day for jour in temps]))
    jours.sort()
    nf_min = MITM+str(annee)+"_"+str(mois)+".png"
    nom_minima_temperatures_mois = os.path.join(DIRECTORY_IMAGES, nf_min)
    minima_par_jour = [min([tempe for i, tempe in enumerate(temperatures) if temps[i].day == jour and type(tempe) == float]) for jour in jours]
    # a = [tempe for jour in jours for i, tempe in enumerate(temperatures) if temps[i].day == jour ]
    # for i in a:
    #    if type(i) != float:
    #        print(type(i))
    plt.axis([0,nombre_jour_par_mois[mois-1], -20, 40])
    plt.grid(True)
    plt.title(u"Temperature minimale en "+conversion_mois[mois-1]+" "+str(annee))
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(jours, minima_par_jour, marker="*")
    plt.savefig(nom_minima_temperatures_mois)
    plt.close()

    nf_max = MATM+str(annee)+"_"+str(mois)+".png"
    nom_maxima_temperatures_mois = os.path.join(DIRECTORY_IMAGES, nf_max)



    maxima_par_jour = [max([tempe for i, tempe in enumerate(temperatures) if temps[i].day == jour and type(tempe) == float]) for jour in jours]

    plt.axis([0,nombre_jour_par_mois[mois-1], -20, 40])
    plt.grid(True)
    plt.title(u"Temperature maximale en "+conversion_mois[mois-1]+" "+str(annee))
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(jours, maxima_par_jour, marker="*")
    plt.savefig(nom_maxima_temperatures_mois)
    plt.close()

    nf_moy = MOTM+str(annee)+"_"+str(mois)+".png"
    nom_moyennes_temperatures_mois = os.path.join(DIRECTORY_IMAGES, nf_moy)
    moyennes_par_jour = [np.mean([tempe for i, tempe in enumerate(temperatures) if temps[i].day == jour and type(tempe) == float]) for jour in jours]
    plt.axis([0, nombre_jour_par_mois[mois-1], -20, 40])
    plt.grid(True)
    plt.title(u"Temperature moyenne en "+conversion_mois[mois-1]+" "+str(annee))
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(jours, moyennes_par_jour, marker="*")
    plt.savefig(nom_moyennes_temperatures_mois)
    plt.close()
    #return nf_min, nf_max, nf_moy


def obtenir_courbe_temperature_annee(temps, temperatures, annee):
    # jour en datetime.datetime.now()
    nf_min = MITA+str(annee)+".png"
    nom_minima = os.path.join(DIRECTORY_IMAGES, nf_min)
    mois_presents = list(set([timme.month for timme in temps]))
    mois_presents.sort()
    minima_mensuels = [min([tempe for j, tempe in enumerate(temperatures) if temps[j].month == i and type(tempe) == float]) for i in mois_presents]
    plt.axis([0,12, -20, 40])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.title(u"Courbe de temperature de l'annee "+str(annee)+".")
    plt.plot(mois_presents, minima_mensuels, marker="*")
    plt.savefig(nom_minima)
    plt.close()

    nf_max = MATA+str(annee)+".png"
    nom_maxima = os.path.join(DIRECTORY_IMAGES, nf_max)
    maxima_mensuels = [max([tempe for j, tempe in enumerate(temperatures) if temps[j].month == i and type(tempe) == float]) for i in mois_presents]
    plt.axis([0,12, -20, 40])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.title(u"Courbe de temperature de l'annee "+str(annee)+".")
    plt.plot(mois_presents, maxima_mensuels, marker="*")
    plt.savefig(nom_maxima)
    plt.close()

    nf_moy = MOTA+str(annee)+".png"
    nom_moyennes = os.path.join(DIRECTORY_IMAGES, nf_moy)
    moyennes_mensuels = [np.mean([tempe for j, tempe in enumerate(temperatures) if temps[j].month == i and type(tempe) == float]) for i in mois_presents]
    plt.axis([0,12, -20, 40])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.title(u"Courbe de temperature de l'annee "+str(annee)+".")
    plt.plot(mois_presents, moyennes_mensuels, marker="*")
    plt.savefig(nom_moyennes)
    plt.close()

    #return nf_min, nf_max, nf_moy



def obtenir_courbe_humidite_jour(temps, humidites):
    # jour en datetime.datetime.now()
    jour = temps[0]
    jour_semaine = jour.ctime()[:3]
    nf_min = MIHJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
    nom_minima_humidite = os.path.join(DIRECTORY_IMAGES, nf_min)
    temps_minima_par_heure = list(set([timme.hour for timme in temps]))
    temps_minima_par_heure.sort()
    minima_par_heure = [min([humi for i, humi in enumerate(humidites) if temps[i].hour == heure and type(humi) == float]) for heure in temps_minima_par_heure]
    plt.title(u"Courbe d'humidite du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0, 24, 0, 100])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(temps_minima_par_heure, minima_par_heure, marker="*")
    plt.savefig(nom_minima_humidite)
    plt.close()

    nf_max = MAHJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
    nom_maxima_humidite = os.path.join(DIRECTORY_IMAGES, nf_max)
    temps_maxima_par_heure = list(set([timme.hour for timme in temps]))
    temps_maxima_par_heure.sort()
    maxima_par_heure = [max([humi for i, humi in enumerate(humidites) if temps[i].hour == heure and type(humi) == float]) for heure in temps_maxima_par_heure]
    plt.title(u"Courbe d'humidite du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0, 24, 0, 100])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(temps_maxima_par_heure, maxima_par_heure, marker="*")
    plt.savefig(nom_maxima_humidite)
    plt.close()

    nf_moy = MOHJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
    nom_moyennes_humidite = os.path.join(DIRECTORY_IMAGES, nf_moy)
    temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
    temps_moyennes_par_heure.sort()
    moyennes_par_heure = [np.mean([humi for i, humi in enumerate(humidites) if temps[i].hour == heure and type(humi) == float]) for heure in temps_moyennes_par_heure]
    plt.title(u"Courbe d'humidite du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0, 24, 0, 100])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
    plt.savefig(nom_moyennes_humidite)
    plt.close()
    #return nf_min, nf_max, nf_moy


def obtenir_courbe_humidite_mois(temps, humidites, annee, mois):
    # jour en datetime.datetime.now()
    jours = list(set([jour.day for jour in temps]))
    jours.sort()
    nf_min = MIHM+str(annee)+"_"+str(mois)+".png"
    nom_minima_humidites_mois = os.path.join(DIRECTORY_IMAGES, nf_min)
    minima_par_jour = [min([humi for i, humi in enumerate(humidites) if temps[i].day == jour and type(humi) == float]) for jour in jours]
    plt.axis([0, nombre_jour_par_mois[mois-1], 0, 100])
    plt.grid(True)
    plt.title(u"Humidite minimale en "+conversion_mois[mois-1]+" "+str(annee)+".")
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(jours, minima_par_jour, marker="*")
    plt.savefig(nom_minima_humidites_mois)
    plt.close()

    nf_max = MAHM+str(annee)+"_"+str(mois)+".png"
    nom_maxima_humidites_mois = os.path.join(DIRECTORY_IMAGES, nf_max)
    maxima_par_jour = [max([humi for i, humi in enumerate(humidites) if temps[i].day == jour and type(humi) == float]) for jour in jours]
    plt.axis([0, nombre_jour_par_mois[mois-1], 0, 100])
    plt.grid(True)
    plt.title(u"Humidite maximale en "+conversion_mois[mois-1]+" "+str(annee)+".")
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(jours, maxima_par_jour, marker="*")
    plt.savefig(nom_maxima_humidites_mois)
    plt.close()

    nf_moy = +str(annee)+"_"+str(mois)+".png"
    nom_moyennes_humidites_mois = os.path.join(DIRECTORY_IMAGES, nf_moy)
    moyennes_par_jour = [np.mean([humi for i, humi in enumerate(humidites) if temps[i].day == jour and type(humi) == float]) for jour in jours]
    plt.axis([0, nombre_jour_par_mois[mois-1], 0, 100])
    plt.grid(True)
    plt.title(u"Humidite moyenne en "+conversion_mois[mois-1]+" "+str(annee)+".")
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(jours, moyennes_par_jour, marker="*")
    plt.savefig(nom_moyennes_humidites_mois)
    plt.close()

    #return nf_min, nf_max, nf_moy
#[]

def obtenir_courbe_humidite_annee(temps, humidites, annee):
    # jour en datetime.datetime.now()

    mois_presents = list(set([timme.month for timme in temps]))
    mois_presents.sort()

    #temps_repartis_par_mois = [[j for j, te in enumerate(temps) if te.month == i].sort(lambda x: x.day) for i in mois_presents]
    nf_min = MIHA+str(annee)+".png"
    nom_minima = os.path.join(DIRECTORY_IMAGES, nf_min)
    minima_mensuels = [min([humi for j, humi in enumerate(humidites) if temps[j].month == i and type(humi) == float]) for i in mois_presents]
    plt.axis([0,12, 0, 100])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.title(u"Courbe d'humidite de l'annee "+str(annee)+".")
    plt.plot(mois_presents, minima_mensuels, marker="*")
    plt.savefig(nom_minima)
    plt.close()

    nf_max = MAHA+str(annee)+".png"
    nom_maxima = os.path.join(DIRECTORY_IMAGES, nf_max)
    maxima_mensuels = [max([humi for j, humi in enumerate(humidites) if temps[j].month == i and type(humi) == float]) for i in mois_presents]
    plt.axis([0,12, 0, 100])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.title(u"Courbe d'humidite de l'annee "+str(annee)+".")
    plt.plot(mois_presents, maxima_mensuels, marker="*")
    plt.savefig(nom_maxima)
    plt.close()

    nf_moy = MOHA+str(annee)+".png"
    nom_moyennes = os.path.join(DIRECTORY_IMAGES, nf_moy)
    moyennes_mensuels = [np.mean([humi for j, humi in enumerate(humidites) if temps[j].month == i and type(humi) == float]) for i in mois_presents]
    plt.axis([0,12, 0, 100])
    plt.grid(True)
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.title(u"Courbe d'humidite de l'annee "+str(annee)+".")
    plt.plot(mois_presents, moyennes_mensuels, marker="*")
    plt.savefig(nom_moyennes)
    plt.close()

    #return nf_min, nf_max, nf_moy


def obtenir_courbe_global_jour(temperatures, humidites, pressions, temps_temperatures, temps_humidites, temps_pression):
    jour = temps_temperatures[0]
    jour_semaine = jour.ctime()[:3]

    if len(temps_humidites) > 0:
        nom_im_humi = MOHJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
        nom_moyennes_humidite = os.path.join(DIRECTORY_IMAGES, nom_im_humi)
        temps_moyennes_par_heure = list(set([timme.hour for timme in temps_humidites]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure = [np.mean([humi for i, humi in enumerate(humidites) if temps_humidites[i].hour == heure and type(humi) == float]) for heure in temps_moyennes_par_heure]
        plt.title(u"Courbe d'humidite du "+
                  conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
        plt.axis([0, 24, 0, 100])
        plt.grid(True)
        plt.xlabel(u"temps")
        plt.ylabel(u"humidite en %")
        plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
        plt.savefig(nom_moyennes_humidite)
        plt.close()
    else:
        print("Il n'y a pas de données d'humidité de l'air aujourd'hui")

    if len(temps_temperatures) > 0:
        nom_im_temp = MOTJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
        nom_moyennes_temperatures = os.path.join(DIRECTORY_IMAGES, nom_im_temp)
        #nom_moyennes_temperatures = "moyennes_temperature_jour.png"
        temps_moyennes_par_heure = list(set([timme.hour for timme in temps_temperatures]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure = [np.mean([tempe for i, tempe in enumerate(temperatures) if temps_temperatures[i].hour == heure and type(tempe) == float]) for heure in temps_moyennes_par_heure]
        plt.title(u"Courbe de temperature du "+
                  conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
        plt.axis([0,24, -20, 40])
        plt.grid(True)
        plt.xlabel(u"temps")
        plt.ylabel(u"temperature en °C")
        plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
        plt.savefig(nom_moyennes_temperatures)
        plt.close()
    else:
        print("Il n'y a pas de données de température aujourd'hui")

    if len(temps_pression) > 0:
        nom_im_pres = MOPJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
        nom_moyennes_pressions = os.path.join(DIRECTORY_IMAGES, nom_im_pres)
        #nom_moyennes_temperatures = "moyennes_temperature_jour.png"
        temps_moyennes_par_heure = list(set([timme.hour for timme in temps_pression]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure = [np.mean([pres for i, pres in enumerate(pressions) if temps_pression[i].hour == heure and type(pres) == float]) for heure in temps_moyennes_par_heure]
        plt.title(u"Courbe de pression du "+
                  conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
        plt.axis([0,24, 970, 1040])
        plt.grid(True)
        plt.xlabel(u"temps")
        plt.ylabel(u"pression en hPa")
        plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
        plt.savefig(nom_moyennes_pressions)
        plt.close()
    else:
        print("Il n'y a pas de données de pression aujourd'hui")


def creer_courbe_humidite_sol(humidite_sol, temps):
    if len(temps) > 0:
        jour = temps[0]
        jour_semaine = jour.ctime()[:3]
        nom_im_pres = MOHSJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
        nom_moyennes_humidite_sol = os.path.join(DIRECTORY_IMAGES, nom_im_pres)
        #nom_moyennes_temperatures = "moyennes_temperature_jour.png"
        temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure = [np.mean([pres for i, pres in enumerate(humidite_sol) if temps[i].hour == heure and type(pres) == float]) for heure in temps_moyennes_par_heure]
        plt.title(u"Courbe de humidite du sol du "+
                  conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
        plt.axis([0,24, 0, 1023])
        plt.grid(True)
        plt.xlabel(u"Temps")
        plt.ylabel(u"Humidite du sol")
        plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
        plt.savefig(nom_moyennes_humidite_sol)
        plt.close()
    else:
        print("Il n'y a pas de mesure de l'humidité du sol pour aujourd'hui")


def creer_courbe_luminosite_jour(luminosite, temps):
    if len(temps) > 0:
        jour = temps[0]
        jour_semaine = jour.ctime()[:3]
        nom_im_pres = MOLJ+str(jour.year)+"_"+str(jour.month)+"_"+str(jour.day)+".png"
        nom_moyennes_luminosite = os.path.join(DIRECTORY_IMAGES, nom_im_pres)
        #nom_moyennes_temperatures = "moyennes_temperature_jour.png"
        temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure = [np.mean([pres for i, pres in enumerate(luminosite) if temps[i].hour == heure and type(pres) == float]) for heure in temps_moyennes_par_heure]
        plt.title(u"Courbe de luminosite du "+
                  conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
        plt.axis([0,24, 0, 1023])
        plt.grid(True)
        plt.xlabel(u"Temps")
        plt.ylabel(u"Luminosite")
        plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
        plt.savefig(nom_moyennes_luminosite)
        plt.close()
    else:
        print("Il n'y a pas de mesure de luminosité pour aujourd'hui")


    #return nom_im_temp, nom_im_humi, nom_im_pres






