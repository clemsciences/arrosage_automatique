 # -*-coding:utf-8-*-
import sqlite3
import os
import datetime
"""
Module à améliorer pour faire mieux correspondre les tables aux besoins
"""


__author__ = 'besnier'

class RecuperateurDonnees:
    def __init__(self, chemin_base_donnee="/home/pi/arrosage_automatique/arrosage_automatique/arrosage_database.db"):
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CONDITIONS_INTRIEURES(
            compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            temperature REAL,
            date_heure timestamp)
            """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PRESSION_ATMO(
            compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            pression REAL,
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

    def obtenir_derniere_pression(self):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM PRESSION_ATMO
        WHERE compteur IN (SELECT max(compteur) FROM PRESSION_ATMO)
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

    def enregistrer_pression(self, pression):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        connex.execute("""
            INSERT INTO PRESSION_ATMO(pression, date_heure)
            VALUES (?,?);
            """, (pression, datetime.datetime.now()))
        connex.commit()
        connex.close()

    def enregistrer_temperature_interieure(self, temperature_interieure):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        connex.execute("""
            INSERT INTO CONDITIONS_INTRIEURES(temperature, date_heure)
            VALUES (?,?);
            """, (temperature_interieure, datetime.datetime.now() ))
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


    def obtenir_pression_jour(self, annee, mois, jour):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM PRESSION_ATMO
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[2].day == jour and mesure[2].month == mois and
                           mesure[2].year == annee]
        pressions = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[2] for mesure in mesures_voulues]
        connex.close()
        return dates, pressions

    def obtenir_pression_mois(self, annee, mois):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM PRESSION_ATMO
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[2].month == mois and mesure[2].year == annee]
        pressions = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[2] for mesure in mesures_voulues]
        connex.close()
        return dates, pressions

    def obtenir_pression_annee(self, annee):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM PRESSION_ATMO
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[2].year == annee]
        pressions = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[2] for mesure in mesures_voulues]
        connex.close()
        return dates, pressions

    def data_this_day(self, annee, mois, jour):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT date_heure
        FROM PRESSION_ATMO
        """)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[2].day == jour and mesure[2].month == mois and
                           mesure[2].year == annee]
        pressions = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[2] for mesure in mesures_voulues]
        connex.close()
        return dates, pressions
        return dates, pressions

if __name__ == "__main__":
    a = RecuperateurDonnees()
    a.creer_table()