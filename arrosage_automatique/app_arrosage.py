# -*-coding:utf-8-*-
from flask import Flask, render_template
from arrosage_database_manager import RecuperateurDonnees
import numpy as np
import io
import generateur_graphique_meteo


app = Flask(__name__)
recuperateur = RecuperateurDonnees()


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
    _, temperature, humidite, date_heure = recuperateur.obtenir_derniere_mesure_meteo()
    return render_template("meteo_maintenant.html", temperature=temperature, humidite=humidite, date_heure=date_heure)


@app.route("/rapport_etat_systeme")
def rapport_etat():
    _, date_dernier_arrosage, _ = recuperateur.obtenir_dernier_arrosage()
    date_derniere_mesure_meteo, _, _, _ = recuperateur.obtenir_derniere_mesure_meteo()
    arduino_branche_present = True

    return render_template("rapport_etat.html", date_dernier_arrosage=date_dernier_arrosage,
                           date_derniere_mesure_meteo=date_derniere_mesure_meteo,
                           arduino_branche_present=arduino_branche_present)




#Obtenir la page web pour une journée, un mois ou une année en particulier.
@app.route("/temperature/<int:annee>/<int:mois>/<int:jour>")
def get_temperature_jour(annee, mois, jour):
    temps, temperatures = recuperateur.obtenir_temperature_jour(annee, mois, jour)
    print len(temps), len(temperatures)
    nom_image_min, nom_image_max, nom_image_moyenne = generateur_graphique_meteo.obtenir_courbe_temperature_jour(temps, temperatures)
    return render_template("affichage_temperature_jour.html", nom_image_min=nom_image_min, nom_image_max=nom_image_max,
                           nom_image_moyenne=nom_image_moyenne)

@app.route("/temperature/<int:annee>/<int:mois>")
def get_temperature_mois(annee, mois):
    temps, temperatures = recuperateur.obtenir_temprature_mois(annee, mois)
    nom_image_min, nom_image_max, nom_image_moyenne = generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
    return render_template("affichage_temperature_mois.html", nom_image_min=nom_image_min, nom_image_max=nom_image_max,
                           nom_image_moyenne=nom_image_moyenne)

@app.route("/temperature/<int:annee>")
def get_temperature_annee(annee):
    l_indices_mois = range(12)
    mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre",
                       "novembre", "decembre"]
    temps, temperatures = recuperateur.obtenir_temprature_annee(annee)
    nom_image_min, nom_image_max, nom_image_moyenne = generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
    mois_presents = list(set([timme.month for timme in temps]))
    truc_pour_page_web = []
    for timme in range(1,13):
        if timme in mois_presents:
            truc_pour_page_web.append(np.mean([tempe for j, tempe in enumerate(temperatures) if temps[j].month == timme]))
        else:
            truc_pour_page_web.append("non mesure")
    return render_template("affichage_temperature_annee.html", l_indices_mois=l_indices_mois, mois=mois, chemin="/home/pi/arrosage_automatique/arrosage_automatique/static/images",
                           nom_image_min=nom_image_min, nom_image_max=nom_image_max,
                           nom_image_moyenne=nom_image_moyenne, temperatures_moyennes_mois=truc_pour_page_web, annee=annee)



@app.route("/humidite/<int:annee>/<int:mois>/<int:jour>")
def get_humidite_jour(annee, mois, jour):
    temps, humidites = recuperateur.obtenir_humidite_jour(annee, mois, jour)
    nom_image_min, nom_image_max, nom_image_moyenne = generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
    return render_template("affichage_humidite_jour.html", nom_image_min=nom_image_min, nom_image_max=nom_image_max,
                           nom_image_moyenne=nom_image_moyenne)

@app.route("/humidite/<int:annee>/<int:mois>")
def get_humidite_mois(annee, mois):
    temps, humidites = recuperateur.obtenir_humidite_mois(annee, mois)
    nom_image_min, nom_image_max, nom_image_moyenne = generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
    return render_template("affichage_humidite_mois.html", nom_image_min=nom_image_min, nom_image_max=nom_image_max,
                           nom_image_moyenne=nom_image_moyenne)

@app.route("/humidite/<int:annee>")
def get_humidite_annee(annee):
    l_indices_mois = range(12)
    mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre",
                       "novembre", "decembre"]
    temps, humidites = recuperateur.obtenir_humidite_annee(annee)
    nom_image_min, nom_image_max, nom_image_moyenne = generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
    mois_presents = list(set([timme.month for timme in temps]))
    truc_pour_page_web = []
    for timme in range(1,13):
        if timme in mois_presents:
            truc_pour_page_web.append(np.mean([tempe for j, tempe in enumerate(humidites) if temps[j].month == timme]))
        else:
            truc_pour_page_web.append("non mesure")

    return render_template("affichage_humidite_annee.html", l_indices_mois=l_indices_mois, mois=mois,
                           nom_image_min=nom_image_min, nom_image_max=nom_image_max,
                           nom_image_moyenne=nom_image_moyenne, humidites_moyennes_mois=truc_pour_page_web)


# Obtenir images tout simplement

@app.route("/temperature/image/<int:annee>/<int:mois>/<int:jour>/<string:genre>")
def get_temperature_jour_image(annee, mois, jour, genre="moyenne"):
    temps, temperatures = recuperateur.obtenir_temperature_jour(annee, mois, jour)
    print temps
    print temperatures
    if genre == "min":
        nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_temperature_jour(temps, temperatures)
    elif genre == "max":
        _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_temperature_jour(temps, temperatures)
    else:
        _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_temperature_jour(temps, temperatures)
    with open(nom_image, "rb") as f:
        image = io.BytesIO()
        image.write(f)
        return image.getvalue()

@app.route("/temperature/image/<int:annee>/<int:mois>/<string:genre>")
def get_temperature_mois_image(annee=2016, mois=10, genre="moyenne"):
    temps, temperatures = recuperateur.obtenir_humidite_mois(annee, mois)
    if genre == "min":
        nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
    elif genre == "max":
        _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
    else:
        _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_temperature_mois(temps, temperatures, annee, mois)
    with open(nom_image, "rb") as f:
        image = io.BytesIO()
        image.write(f)
        return image.getvalue()

@app.route("/temperature/image/<int:annee>")
def get_temperature_annee_image(annee, genre="moyenne"):
    temps, temperatures = recuperateur.obtenir_temprature_annee(annee)
    if genre == "min":
        nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
    elif genre == "max":
        _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
    else:
        _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_temperature_annee(temps, temperatures, annee)
    with open(nom_image, "rb") as f:
        image = io.BytesIO()
        image.write(f)
        return image.getvalue()



@app.route("/humidite/image/<int:annee>/<int:mois>/<int:jour>/<string:genre>")
def get_humidite_jour_image(annee, mois, jour, genre="moyenne"):
    temps, humidites = recuperateur.obtenir_humidite_jour(annee, mois, jour)
    if genre == "min":
        nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
    elif genre == "max":
        _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
    else:
        _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_humidite_jour(temps, humidites)
    with open(nom_image, "rb") as f:
        image = io.BytesIO()
        image.write(f)
        return image.getvalue()

@app.route("/humidite/image/<int:annee>/<int:mois>/<string:genre>")
def get_humidite_mois_image(annee, mois, genre="moyenne"):
    temps, humidites = recuperateur.obtenir_humidite_mois(annee, mois)
    if genre == "min":
        nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
    elif genre == "max":
        _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
    else:
        _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_humidite_mois(temps, humidites, annee, mois)
    with open(nom_image, "rb") as f:
        image = io.BytesIO()
        image.write(f)
        return image.getvalue()

@app.route("/humidite/image/<int:annee>/<string:genre>")
def get_humidite_annee_image(annee, genre="moyenne"):
    temps, humidites = recuperateur.obtenir_humidite_annee(annee)
    if genre == "min":
        nom_image, _, _ = generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
    elif genre == "max":
        _, nom_image, _ = generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
    else:
        _, _, nom_image = generateur_graphique_meteo.obtenir_courbe_humidite_annee(temps, humidites, annee)
    with open(nom_image, "rb") as f:
        image = io.BytesIO()
        image.write(f)
        return image.getvalue()




if __name__ == "__main__":
    app.run(debug=True)
