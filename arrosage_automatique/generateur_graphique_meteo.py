# -*-coding:utf-8-*-
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
DIRECTORY = "images"
conversion_mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
                       "novembre", "décembre"]

conversion_jour = {"Mon" : "Lundi", "Tue" : "Mardi", "Wed" : "Mercredi", "Thu" : "Jeudi", "Fri" : "Vendredi",
                       "Sat" : "Samedi", "Sun" : "Dimanche"}

def obtenir_courbe_temperature_jour(temps, temperatures):
    # jour en datetime.datetime.now()
    jour = temps[0]
    jour_semaine = jour.ctime()[:3]
    nom_minima_temperature = "minima_temperature_jour.png"
    temps_minima_par_heure = list(set([timme.hour for timme in temps]))
    temps_minima_par_heure.sort()
    minima_par_heure = [min([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure]) for heure in temps_minima_par_heure]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.xlabel("temps")
    plt.ylabel("temperature en °C")
    plt.plot(temps_minima_par_heure, minima_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_minima_temperature))

    nom_maxima_temperature = "maxima_temperature_jour.png"
    temps_maxima_par_heure = list(set([timme.hour for timme in temps]))
    temps_maxima_par_heure.sort()
    maxima_par_heure = [max([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure]) for heure in temps_maxima_par_heure]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(temps_maxima_par_heure, maxima_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_maxima_temperature))

    nom_moyennes_temperatures = "moyennes_temperature_jour.png"
    temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
    temps_moyennes_par_heure.sort()
    moyennes_par_heure = [np.mean([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure]) for heure in temps_moyennes_par_heure]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_moyennes_temperatures))
    return nom_minima_temperature, nom_maxima_temperature, nom_moyennes_temperatures


def obtenir_courbe_temperature_mois(temps, temperatures, annee, mois):
    # jour en datetime.datetime.now()
    jours = list(set([jour.day for jour in temps])).sort()
    nom_minima_temperatures_mois = "minima_temperature_mois.png"
    minima_par_jour = [min([tempe for i, tempe in enumerate(temperatures) if temps[i].day == jour]) for jour in jours]
    plt.axis([0,24, -20, 40])
    plt.title(u"Temperature minimale en "+conversion_mois[mois]+" "+str(annee))
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(jours, minima_par_jour, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_minima_temperatures_mois))
    nom_maxima_temperatures_mois = "maxima_temperature_mois.png"
    maxima_par_jour = [max([tempe for i, tempe in enumerate(temperatures) if temps[i].day == jour]) for jour in jours]
    plt.axis([0,24, -20, 40])
    plt.title(u"Temperature maximale en "+conversion_mois[mois]+" "+str(annee))
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(jours, maxima_par_jour, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_maxima_temperatures_mois))
    nom_moyennes_temperatures_mois = "moyennes_temperature_mois.png"
    moyennes_par_jour = [np.mean([tempe for i, tempe in enumerate(temperatures) if temps[i].day == jour]) for jour in jours]
    plt.axis([0,24, -20, 40])
    plt.title(u"Temperature moyenne en "+conversion_mois[mois]+" "+str(annee))
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.plot(jours, moyennes_par_jour, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_moyennes_temperatures_mois))
    return nom_minima_temperatures_mois, nom_maxima_temperatures_mois, nom_moyennes_temperatures_mois


def obtenir_courbe_temperature_annee(temps, temperatures, annee):
    # jour en datetime.datetime.now()
    nom_minima = "nom_temperature_annee_minima.png"
    minima_mensuels = [min([tempe for j, tempe in enumerate(temperatures) if temps[j].month == i]) for i in range(12)]
    plt.axis([0,12, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.title(u"Courbe de temperature de l'annee "+str(annee)+".")
    plt.plot(range(12), minima_mensuels, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_minima))
    nom_maxima = "nom_temperature_annee_maxima.png"
    maxima_mensuels = [max([tempe for j, tempe in enumerate(temperatures) if temps[j].month == i]) for i in range(12)]
    plt.axis([0,12, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.title(u"Courbe de temperature de l'annee "+str(annee)+".")
    plt.plot(range(12), maxima_mensuels, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_maxima))
    nom_moyennes = "nom_temperature_annee_moyennes.png"
    moyennes_mensuels = [np.mean([tempe for j, tempe in enumerate(temperatures) if temps[j].month == i]) for i in range(12)]
    plt.axis([0,12, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    plt.title(u"Courbe de temperature de l'annee "+str(annee)+".")
    plt.plot(range(12), moyennes_mensuels, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_moyennes))
    return nom_minima, nom_maxima, nom_moyennes



def obtenir_courbe_humidite_jour(temps, humidites):
    # jour en datetime.datetime.now()
    jour = temps[0]
    jour_semaine = jour.ctime()[:3]
    nom_minima_humidite = "minima_humidite_jour.png"
    temps_minima_par_heure = list(set([timme.hour for timme in temps]))
    temps_minima_par_heure.sort()
    minima_par_heure = [min([humi for i, humi in enumerate(humidites) if temps[i].hour == heure]) for heure in temps_minima_par_heure]
    plt.title(u"Courbe d'humidite du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0, 24, 0, 100])
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(temps_minima_par_heure, minima_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_minima_humidite))

    nom_maxima_humidite = "maxima_humidite_jour.png"
    temps_maxima_par_heure = list(set([timme.hour for timme in temps]))
    temps_maxima_par_heure.sort()
    maxima_par_heure = [max([humi for i, humi in enumerate(humidites) if temps[i].hour == heure]) for heure in temps_maxima_par_heure]
    plt.title(u"Courbe d'humidite du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0, 24, 0, 100])
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(temps_maxima_par_heure, maxima_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_maxima_humidite))

    nom_moyennes_humidite = "moyennes_humidite_jour.png"
    temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
    temps_moyennes_par_heure.sort()
    moyennes_par_heure = [np.mean([humi for i, humi in enumerate(humidites) if temps[i].hour == heure]) for heure in temps_moyennes_par_heure]
    plt.title(u"Courbe d'humidite du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0, 24, 0, 100])
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_moyennes_humidite))
    return nom_minima_humidite, nom_maxima_humidite, nom_moyennes_humidite


def obtenir_courbe_humidite_mois(temps, humidites, annee, mois):
    # jour en datetime.datetime.now()
    jours = list(set([jour.day for jour in temps]))
    jours.sort()
    nom_minima_humidites_mois = "minima_humidite_mois.png"
    minima_par_jour = [min([humi for i, humi in enumerate(humidites) if temps[i].day == jour]) for jour in jours]
    plt.axis([0, len(jours), 0, 100])
    plt.title(u"Humidite minimale en "+conversion_mois[mois]+" "+annee+".")
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(jours, minima_par_jour, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_minima_humidites_mois))
    nom_maxima_humidites_mois = "maxima_humidite_mois.png"
    maxima_par_jour = [max([humi for i, humi in enumerate(humidites) if temps[i].day == jour]) for jour in jours]
    plt.axis([0, len(jours), 0, 100])
    plt.title(u"Humidite maximale en "+conversion_mois[mois]+" "+annee+".")
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(jours, maxima_par_jour, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_maxima_humidites_mois))
    nom_moyennes_humidites_mois = "moyennes_humidite_mois.png"
    moyennes_par_jour = [np.mean([humi for i, humi in enumerate(humidites) if temps[i].day == jour]) for jour in jours]
    plt.axis([0, len(jours), 0, 100])
    plt.title(u"Humidite moyenne en "+conversion_mois[mois]+" "+annee+".")
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.plot(jours, moyennes_par_jour, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_moyennes_humidites_mois))
    return nom_minima_humidites_mois, nom_maxima_humidites_mois, nom_moyennes_humidites_mois
#[]

def obtenir_courbe_humidite_annee(temps, humidites, annee):
    # jour en datetime.datetime.now()

    mois_presents = list(set([timme.month for timme in temps]))
    mois_presents.sort()

    temps_repartis_par_mois = [[j for j, te in enumerate(temps) if te.month == i].sort(lambda x: x.day) for i in mois_presents]

    nom_minima = "nom_humidite_annee_minima.png"
    minima_mensuels = [min([humi for j, humi in enumerate(humidites) if temps[j].month == i]) for i in mois_presents]
    plt.axis([0,12, 0, 100])
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.title(u"Courbe d'humidite de l'annee "+str(annee)+".")
    plt.plot(range(12), minima_mensuels, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_minima))
    nom_maxima = "nom_humidite_annee_maxima.png"
    maxima_mensuels = [max([humi for j, humi in enumerate(humidites) if temps[j].month == i]) for i in mois_presents]
    plt.axis([0,12, 0, 100])
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.title(u"Courbe d'humidite de l'annee "+str(annee)+".")
    plt.plot(range(12), maxima_mensuels, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_maxima))
    nom_moyennes = "nom_humidite_annee_moyennes.png"
    moyennes_mensuels = [np.mean([humi for j, humi in enumerate(humidites) if temps[j].month == i]) for i in mois_presents]
    plt.axis([0,12, 0, 100])
    plt.xlabel(u"temps")
    plt.ylabel(u"humidite en %")
    plt.title(u"Courbe d'humidite de l'annee "+str(annee)+".")
    plt.plot(range(12), moyennes_mensuels, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_moyennes))
    return nom_minima, nom_maxima, nom_moyennes


