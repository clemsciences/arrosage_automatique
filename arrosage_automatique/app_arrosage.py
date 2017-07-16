# -*-coding:utf-8-*-
from flask import Flask, render_template, jsonify, send_file
from arrosage_database_manager import RecuperateurDonnees
import numpy as np
import io
import generateur_graphique_meteo
import datetime
import collections, pickle
import mimetypes

import os

from constantes import *

__author__ = "__author__ = 'besnier'"


chemin_images = "/home/pi/arrosage_automatique/arrosage_automatique/static/images"
app = Flask(__name__)
recuperateur = RecuperateurDonnees() #'C:\\Users\\Clément\\PycharmProjects\\arrosage_automatique\\arrosage_automatique\\arrosage_database.db')
l_mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre",
                       "novembre", "decembre"]

@app.route("/")
def accueil():
    return render_template('accueil.html')


@app.route('/parametrage_arrosage/')
def parametrage_arrosage():
    return render_template("conditions_arrosages.html")


@app.route('/statistiques_meteo/')
def statistiques_meteorologique():
    return render_template("statistiques_meteo.html")


@app.route('/statistiques_arrosages/')
def statistiques_arrosage():
    return render_template("statistiques_arrosages.html")


@app.route('/rapport_courriel/')
def rapport_courriel():
    return render_template("rapport_courriel.html")


@app.route("/meteo_maintenant/")
def meteo_maintenant():
    _, temperature, date_heure = recuperateur.obtenir_derniere_mesure_meteo(d_code_table_capteurs["TE"])
    _, humidite, _ = recuperateur.obtenir_derniere_mesure_meteo(d_code_table_capteurs["HA"])
    _, pression, _ = recuperateur.obtenir_derniere_pression(d_code_table_capteurs["PR"])
    return render_template("meteo_maintenant.html", temperature=temperature, humidite=humidite, date_heure=date_heure, pression=pression)


@app.route("/rapport_etat_systeme")
def rapport_etat():
    _, date_dernier_arrosage, _ = recuperateur.obtenir_dernier_arrosage()
    date_derniere_mesure_meteo, _, _, _ = recuperateur.obtenir_derniere_mesure_meteo()
    arduino_branche_present = True

    return render_template("rapport_etat.html", date_dernier_arrosage=date_dernier_arrosage,
                           date_derniere_mesure_meteo=date_derniere_mesure_meteo,
                           arduino_branche_present=arduino_branche_present)


@app.route("/le_comment_c_est_fait")
def le_comment_c_est_fait():
    return render_template("le_comment_c_est_fait.html")


@app.route("/les_chats")
def voir_les_chats():
    return render_template("les_chats.html")

#Obtenir la page web pour une journée, un mois ou une année en particulier.
@app.route("/temperature/<int:annee>/<int:mois>/<int:jour>")
def get_temperature_jour(annee, mois, jour):
    temps, temperatures = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["TE"])
    generateur_graphique_meteo.obtenir_courbe_temperature_jour(temps, temperatures)
    return render_template("affichage_temperature_jour.html", nom_image_min=nommer_jour(MITJ, annee, mois, jour), nom_image_max=nommer_jour(MATJ, annee, mois, jour),
                           nom_image_moyenne=nommer_jour(MOTJ, annee, mois, jour), annee=annee, mois=l_mois[mois-1], jour=jour)

@app.route("/temperature/<int:annee>/<int:mois>")
def get_temperature_mois(annee, mois):
    temps, temperatures = recuperateur.obtenir_mesures_mois(annee, mois, d_code_table_capteurs["TE"])
    generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
    return render_template("affichage_temperature_mois.html", nom_image_min=nommer_mois(MITM, annee, mois), nom_image_max=nommer_mois(MATM, annee, mois),
                           nom_image_moyenne=nommer_mois(MOTM, annee, mois), mois=l_mois[mois-1], annee=annee)

@app.route("/temperature/<int:annee>")
def get_temperature_annee(annee):
    l_indices_mois = range(12)

    temps, temperatures = recuperateur.obtenir_mesures_annee(annee, d_code_table_capteurs["TE"])
    generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
    mois_presents = list(set([timme.month for timme in temps]))
    truc_pour_page_web = []
    for timme in range(1,13):
        if timme in mois_presents:
            truc_pour_page_web.append(np.mean([tempe for j, tempe in enumerate(temperatures) if temps[j].month == timme and type(tempe) == float]))
        else:
            truc_pour_page_web.append("non mesure")
    return render_template("affichage_temperature_annee.html", l_indices_mois=l_indices_mois, mois=l_mois,
                           nom_image_min=nommer_annee(MITA, annee), nom_image_max=nommer_annee(MATA, annee),
                           nom_image_moyenne=nommer_annee(MOTA, annee), temperatures_moyennes_mois=truc_pour_page_web, annee=annee)



@app.route("/humidite/<int:annee>/<int:mois>/<int:jour>")
def get_humidite_jour(annee, mois, jour):
    temps, humidites = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["HA"])
    generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
    return render_template("affichage_humidite_jour.html", nom_image_min=nommer_jour(MIHJ, annee, mois, jour), nom_image_max=nommer_jour(MAHJ, annee, mois, jour),
                           nom_image_moyenne=nommer_jour(MOHJ, annee, mois, jour), annee=annee, mois=l_mois[mois-1], jour=jour)

@app.route("/humidite/<int:annee>/<int:mois>")
def get_humidite_mois(annee, mois):
    temps, humidites = recuperateur.obtenir_mesures_mois(annee, mois, d_code_table_capteurs["HA"])
    generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
    return render_template("affichage_humidite_mois.html", nom_image_min=nommer_mois(MIHM, annee, mois), nom_image_max=nommer_mois(MAHM, annee, mois),
                           nom_image_moyenne=nommer_mois(MOHM, annee, mois), mois=l_mois[mois-1], annee=annee)

@app.route("/humidite/<int:annee>")
def get_humidite_annee(annee):
    l_indices_mois = range(12)
    temps, humidites = recuperateur.obtenir_mesures_annee(annee, d_code_table_capteurs["HA"])
    generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
    mois_presents = list(set([timme.month for timme in temps]))
    truc_pour_page_web = []
    for timme in range(1,13):
        if timme in mois_presents:
            truc_pour_page_web.append(np.mean([tempe for j, tempe in enumerate(humidites) if temps[j].month == timme]))
        else:
            truc_pour_page_web.append("non mesure")

    return render_template("affichage_humidite_annee.html", l_indices_mois=l_indices_mois, mois=l_mois,
                           nom_image_min=nommer_annee(MIHA, annee), nom_image_max=nommer_annee(MAHA, annee),
                           nom_image_moyenne=nommer_annee(MOHA, annee), humidites_moyennes_mois=truc_pour_page_web, annee=annee)

# Obtenir toutes les infos météo valide que pour une journée
@app.route("/aujourdhui")
def get_global_aujourdhui():
    maintenant = datetime.datetime.now()
    return get_global_jour(maintenant.year, maintenant.month, maintenant.day)




# Obtenir toutes les infos météo valide que pour une journée
@app.route("/global/<int:annee>/<int:mois>/<int:jour>")
def get_global_jour(annee, mois, jour):
    nom_image_temperature = nommer_jour(MOTJ, annee, mois, jour)
    nom_image_humidite = nommer_jour(MOHJ, annee, mois, jour)
    nom_image_pression = nommer_jour(MOPJ, annee, mois, jour)
    dossiers_images = os.listdir(DIRECTORY_IMAGES)

    if nom_image_humidite not in dossiers_images or nom_image_pression not in dossiers_images or nom_image_temperature not in dossiers_images:
        temps, temperatures = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["TE"])
        temps, humidites = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["HA"])
        temps_pression, pressions = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["PR"])
        generateur_graphique_meteo.obtenir_courbe_global_jour(temps, temperatures, humidites, pressions, temps_pression)


    return render_template("affichage_global_jour.html", nom_image_temperature=nom_image_temperature,
                           nom_image_humidite=nom_image_humidite, nom_image_pression=nom_image_pression,
                           annee=annee, mois=l_mois[mois-1], jour=jour)

# API REST

@app.route("/data/<int:annee>/<int:mois>/<int:jour>")
def get_data_global_jour(annee, mois, jour):
    nom_fichier_json = nommer_jour_json("data_jour_", str(annee), str(mois), str(jour))
    if nom_fichier_json not in os.listdir(DIRECTORY_JSON):
        temps, temperatures = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["TE"])
        temps, humidites = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["HA"])
        temps_pression, pressions = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["PR"])

        temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure_temperature = collections.defaultdict(str)
        moyennes_par_heure_temperature.update({heure : str(float(np.mean([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure and type(tempe) == float])))[:5] for heure in temps_moyennes_par_heure})

        temps_moyennes_par_heure = list(set([timme.hour for timme in temps]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure_humidite = collections.defaultdict(str)

        moyennes_par_heure_humidite.update({heure : str(float(np.mean([humi for i, humi in enumerate(humidites) if temps[i].hour == heure and type(humi) == float])))[:5] for heure in temps_moyennes_par_heure})

        #d["humidite"] = moyennes_par_heure_humidite
        temps_moyennes_par_heure = list(set([timme.hour for timme in temps_pression]))
        temps_moyennes_par_heure.sort()
        moyennes_par_heure_pression = collections.defaultdict()
        moyennes_par_heure_pression.update({heure: str(float(np.mean([pres for i, pres in enumerate(pressions) if temps_pression[i].hour == heure and type(pres) == float])))[:7] for heure in temps_moyennes_par_heure})

        #d['pression'] = moyennes_par_heure_pression
        d = {heure : {'humidite': moyennes_par_heure_humidite[heure], 'pression': moyennes_par_heure_pression[heure],"temperature": moyennes_par_heure_temperature[heure]} for heure in temps_moyennes_par_heure}
        with open(os.path.join(DIRECTORY_JSON, nom_fichier_json), "wb") as f:
            myp = pickle.Pickler(f)
            myp.dump(d)

    with open(os.path.join(DIRECTORY_JSON, nom_fichier_json), "rb") as f:
        myp = pickle.Unpickler(f)
        d = myp.load()
    return jsonify(d)


@app.route("/data/aujourdhui")
def get_data_global_aujourdhui():
    maintenant = datetime.datetime.now()
    annee, mois, jour = maintenant.year, maintenant.month, maintenant.day
    return get_data_global_jour(annee, mois, jour)



# Obtenir images tout simplement

@app.route("/image/<grandeur>/<int:annee>/<int:mois>/<int:jour>")
def get_data_jour_image(grandeur, annee, mois, jour):
    if grandeur == "temperature":
        nom_image = nommer_jour(MOTJ, annee, mois, jour)
    elif grandeur == "humidite":
        nom_image = nommer_jour(MOHJ, annee, mois, jour)
    elif grandeur == "pression":
        nom_image = nommer_jour(MOPJ, annee, mois, jour)
    else:
        return None
    dossiers_images = os.listdir(DIRECTORY_IMAGES)

    if nom_image not in dossiers_images:
        temps, temperatures = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["TE"])
        temps, humidites = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["HA"])
        temps_pression, pressions = recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["PR"])
        generateur_graphique_meteo.obtenir_courbe_global_jour(temps, temperatures, humidites, pressions, temps_pression)
    chemin_et_nom_fichier = os.path.join(DIRECTORY_IMAGES, nom_image)
    return send_file(chemin_et_nom_fichier, "image/png")

#
#
# @app.route("/temperature/image/<int:annee>/<int:mois>/<string:genre>")
# def get_temperature_mois_image(annee=2016, mois=10, genre="moyenne"):
#     temps, temperatures = recuperateur.obtenir_humidite_mois(annee, mois)
#     if genre == "min":
#         nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
#     elif genre == "max":
#         _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
#     else:
#         _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
#     with open(os.path.join(chemin_images, nom_image), "rb") as f:
#         image = io.BytesIO()
#         image.write(f)
#         return image.getvalue()
#
# @app.route("/temperature/image/<int:annee>")
# def get_temperature_annee_image(annee, genre="moyenne"):
#     temps, temperatures = recuperateur.obtenir_temprature_annee(annee)
#     if genre == "min":
#         nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
#     elif genre == "max":
#         _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
#     else:
#         _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
#     with open(os.path.join(chemin_images, nom_image), "rb") as f:
#         image = io.BytesIO()
#         image.write(f)
#         return image.getvalue()
#
#
#
# @app.route("/humidite/image/<int:annee>/<int:mois>/<int:jour>/<string:genre>")
# def get_humidite_jour_image(annee, mois, jour, genre="moyenne"):
#     temps, humidites = recuperateur.obtenir_humidite_jour(annee, mois, jour)
#     if genre == "min":
#         nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
#     elif genre == "max":
#         _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
#     else:
#         _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
#     with open(os.path.join(chemin_images, nom_image), "rb") as f:
#         image = io.BytesIO()
#         image.write(f)
#         return image.getvalue()
#
# @app.route("/humidite/image/<int:annee>/<int:mois>/<string:genre>")
# def get_humidite_mois_image(annee, mois, genre="moyenne"):
#     temps, humidites = recuperateur.obtenir_humidite_mois(annee, mois)
#     if genre == "min":
#         nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
#     elif genre == "max":
#         _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
#     else:
#         _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
#     with open(os.path.join(chemin_images, nom_image), "rb") as f:
#         image = io.BytesIO()
#         image.write(f)
#         return image.getvalue()
#
# @app.route("/humidite/image/<int:annee>/<string:genre>")
# def get_humidite_annee_image(annee, genre="moyenne"):
#     temps, humidites = recuperateur.obtenir_humidite_annee(annee)
#     if genre == "min":
#         nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
#     elif genre == "max":
#         _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
#     else:
#         _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
#     with open(os.path.join(chemin_images, nom_image), "rb") as f:
#         image = io.BytesIO()
#         image.write(f)
#         return image.getvalue()
#
# rb


if __name__ == "__main__":
    app.run(debug=True)
