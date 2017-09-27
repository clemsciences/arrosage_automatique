 # -*-coding:utf-8-*-
import sqlite3
import os
import datetime
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
DIRECTORY = "/home/pi/arrosage_automatique/arrosage_automatique/static/images"
conversion_mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
                       "novembre", "décembre"]

conversion_jour = {"Mon" : "Lundi", "Tue" : "Mardi", "Wed" : "Mercredi", "Thu" : "Jeudi", "Fri" : "Vendredi",
                       "Sat" : "Samedi", "Sun" : "Dimanche"}

def obtenir_courbe_temperature_jour(temps, temperatures):
    # jour en datetime.datetime.now()
    jour = temps[0]
    jour_semaine = jour.ctime()[:3]
    nom_minima_temperature = "minima_temperature_jour.png"
    tmph = list(set([timme.hour for timme in temps]))
    tmph.sort()
    print "ensemble heures", set([temps[i].hour for i, tempe in enumerate(temperatures)])
    minima_par_heure = [min([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure]) for heure in tmph]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    #p2 = plt.plot(temps_minima_par_heure, minima_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_minima_temperature))

    nom_maxima_temperature = "maxima_temperature_jour.png"
    temps_maxima_par_heure = range(24)
    maxima_par_heure = [max([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure]) for heure in tmph]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    #p2 = plt.plot(temps_maxima_par_heure, maxima_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_maxima_temperature))

    nom_moyennes_temperatures = "moyennes_temperature_jour.png"
    temps_moyennes_par_heure = range(24)
    moyennes_par_heure = [np.mean([tempe for i, tempe in enumerate(temperatures) if temps[i].hour == heure]) for heure in tmph]
    plt.title(u"Courbe de temperature du "+
              conversion_jour[jour_semaine]+" "+str(jour.day)+" "+conversion_mois[jour.month-1]+".")
    plt.axis([0,24, -20, 40])
    plt.xlabel(u"temps")
    plt.ylabel(u"temperature en °C")
    #p2 = plt.plot(temps_moyennes_par_heure, moyennes_par_heure, marker="*")
    plt.savefig(os.path.join(DIRECTORY, nom_moyennes_temperatures))
    return nom_minima_temperature, nom_maxima_temperature, nom_moyennes_temperatures

class RecuperateurDonnees:
    def __init__(self, chemin_base_donnee="arrosage_database.db"):
        assert isinstance(chemin_base_donnee, str)
        self.chemin_base_donnee = chemin_base_donnee
        if not os.path.isfile(self.chemin_base_donnee):
            self.creer_table()
            os.system("chmod 777 arrosage_database.db")

    def creer_table(self):
        conn = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()
        cursor.execute("""
		CREATE TABLE IF NOT EXISTS CONDITIONS_ARROSAGE(
		compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		temperature_min REAL,
		humidite_max REAL,
		frequence_min REAL,
		heure_min INTEGER,
		heure_max INTEGER,
		duree INTEGER,
		date_heure timestamp )
		""")
        # timestamp : datetime.datetime.now()
        # duree en secondes
        cursor.execute("""
		CREATE TABLE IF NOT EXISTS ARROSAGE(
		compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		date_heure timestamp,
		duree INTEGER)
		""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS COURRIEL(
            compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            emmeteur TEXT,
            recepteur TEXT,
            objet TEXT,
            texte TEXT,
            date_heure timestamp)
		""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CONDITIONS_METEOROLOGIQUES(
            compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            temperature REAL,
            humidite REAL,
            date_heure timestamp)
		""")
        conn.commit()
        conn.close()

    def enregistrer_courriel(self, emetteur, recepteur, objet, texte):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        connex.execute("""
            INSERT INTO COURRIEL(emetteur, recepteur, objet, texte)
            VALUES (?,?,?,?);
            """, (emetteur, recepteur, objet, texte))
        connex.commit()
        connex.close()
    def obtenir_conditions_meteorologiques_depuis(self, jours):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        """)
        #connex.commit()
        #[compteur, date, temperature, humidite] = cursor.fetchone()
        res = cursor.fetchall()
        print res[0]
        res = [(i[0],i[1], i[2]) for i in res if datetime.timedelta.total_seconds(i.date - datetime.datetime.now()) < jours*86400]
        #res = []
        connex.close()
        return res

    def obtenir_conditions_meteorologiques(self):
        """
        Connexion à la base de données pour obtenir les derniers relevés de la situation météorologique
        :return:
        """

        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        WHERE compteur IN  (SELECT max(compteur) FROM CONDITIONS_METEOROLOGIQUES)
        """)

        #connex.commit()
        # [compteur, temperature, humidite, date] = cursor.fetchone()
        res = cursor.fetchone()
        connex.close()
        return res

    def enregistrer_arrosage(self, duree):
        """
        Remplit la table Arrosage à chaque fin d'arrosage
        :param duree : durée de l'arrosage
        :return:
        """
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        connex.execute("""
            INSERT INTO ARROSAGE(date_heure, duree)
            VALUES (?,?);
            """, (datetime.datetime.now(), str(duree)))
        connex.commit()
        connex.close()

    def obtenir_dernier_arrosage(self):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
            SELECT *
            FROM  ARROSAGE
            WHERE compteur IN (SELECT max(compteur) FROM ARROSAGE)
            """)
        res = connex.fetchone()
        connex.close()
        # (date_heure, duree)
        return res

    def obtenir_conditions_arrosage(self):
        """
        Consulte la base de donnée base_arrosage.db pour récupérer les données sur les
        moment adéquat pour arroser
        :return:
        """
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_ARROSAGE
        WHERE compteur IN (SELECT max(compteur) FROM CONDITIONS_ARROSAGE)
        """)

        #connex.commit()
        # [compteur, temperature_min, humidite_max, frequence_min, heure_min, heure_max, duree ] = cursor.fetchone()
        res = cursor.fetchone()
        connex.close()
        return res

    def obtenir_derniere_mesure_meteo(self):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        WHERE compteur IN (SELECT max(compteur) FROM CONDITIONS_METEOROLOGIQUES)
        """)

        #connex.commit()
        # [compteur, temperature, humidite, date_heure = cursor.fetchone()
        res = cursor.fetchone()
        connex.close()
        return res

    def enregistrer_temperature_humidite(self, temperature, humidite):
        # fonction quasiment identique à enregistrer_humidite
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        #cursor.execute("""
        #SELECT compteur
        #FROM ConditionsMeteorologiques
        #WHERE compteur IN (SELECT max(compteur) FROM ConditionsMeteorologiques)
        #""")

        #connex.commit()
        #compteur = cursor.fetchone()
        connex.execute("""
         INSERT INTO CONDITIONS_METEOROLOGIQUES(temperature, humidite, date_heure)
          VALUES (?,?,?);
           """, (str(temperature), str(humidite), datetime.datetime.now())) #  time.asctime(date_exacte)
        connex.commit()
        connex.close()

    def enregistrer_humidite(self, temperature, humidite):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        connex.execute("""
             INSERT INTO CONDITIONS_METEOROLOGIQUES(temperature, humidite, date_heure)
            VALUES (?,?,?);
            """, (str(temperature), str(humidite), datetime.datetime.now()))
        connex.commit()
        connex.close()

    def enregistrer_mesure(self, temperature, humidite):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        connex.execute("""
            INSERT INTO CONDITIONS_METEOROLOGIQUES(temperature, humidite, date_heure)
            VALUES (?,?,?);
            """, (str(temperature), str(humidite), datetime.datetime.now() ))
        connex.commit()
        connex.close()



    # Fonctions pour afficher les graphiques voulus
    def obtenir_temperature_jour(self, annee, mois, jour):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[3].day == jour and mesure[3].month == mois and
                           mesure[3].year == annee]
        temperatures = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[3] for mesure in mesures_voulues]
        connex.close()
        return dates, temperatures

    def obtenir_temprature_mois(self, annee, mois):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[3].month == mois and mesure[3].year == annee]
        temperatures = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[3] for mesure in mesures_voulues]
        connex.close()
        return dates, temperatures


    def obtenir_temprature_annee(self, annee):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[3].year == annee]
        temperatures = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[3] for mesure in mesures_voulues]
        connex.close()
        return dates, temperatures

    def obtenir_humidite_jour(self, annee, mois, jour):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[3].day == jour and mesure[3].month == mois and
                           mesure[3].year == annee]
        humidites = [mesure[2] for mesure in mesures_voulues]
        dates = [mesure[3] for mesure in mesures_voulues]
        connex.close()
        return dates, humidites

    def obtenir_humidite_mois(self, annee, mois):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[3].month == mois and mesure[3].year == annee]
        humidites = [mesure[2] for mesure in mesures_voulues]
        dates = [mesure[3] for mesure in mesures_voulues]
        connex.close()
        return dates, humidites

    def obtenir_humidite_annee(self, annee):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM CONDITIONS_METEOROLOGIQUES
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[3].year == annee]
        humidites = [mesure[2] for mesure in mesures_voulues]
        dates = [mesure[3] for mesure in mesures_voulues]
        connex.close()
        return dates, humidites
if __name__ == "__main__":
    recup = RecuperateurDonnees()
    print recup.obtenir_conditions_meteorologiques()
    #print recup.obtenir_temperature_jour(2016, 9, 25)
    #temps, temperatures = recup.obtenir_temperature_jour(2016, 9, 24)
    #print len(temps), len(temperatures)
    #nom_image_min, nom_image_max, nom_image_moyenne = obtenir_courbe_temperature_jour(temps, temperatures)    
