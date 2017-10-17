 # -*-coding:utf-8-*-

import sqlite3
import os
import datetime
from constantes import *
"""
Module à améliorer pour faire mieux correspondre les tables aux besoins
"""


__author__ = 'besnier'


class RecuperateurDonnees:
    def __init__(self, chemin_base_donnee="/home/pi/arrosage_automatique/arrosage_automatique/mesures_et_arrosages.db"):
        assert isinstance(chemin_base_donnee, str)
        self.chemin_base_donnee = chemin_base_donnee
        if not os.path.isfile(self.chemin_base_donnee):
            self.creer_table()
            os.system("chmod 777 arrosage_database.db")

    def creer_table(self):
        conn = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = conn.cursor()
        cursor.execute("""
		CREATE TABLE IF NOT EXISTS ARROSAGE(
		compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
		date_heure timestamp,
		duree INTEGER)
		""")
        for table in noms_tables_capteurs:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS %s(
            compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            mesure REAL,
            date_heure timestamp)
            """% table)
        conn.commit()
        conn.close()


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


    # Fonctions pour afficher les graphiques voulus

    def obtenir_mesures_jour(self, annee, mois, jour, nom_table):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM %s
        """ % nom_table)

        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[2].day == jour and mesure[2].month == mois and
                           mesure[2].year == annee]
        valeurs = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[2] for mesure in mesures_voulues]
        connex.close()
        return dates, valeurs

    def obtenir_mesures_mois(self, annee, mois, nom_table):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM %s
        """ % nom_table)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[2].month == mois and mesure[2].year == annee]
        valeurs = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[2] for mesure in mesures_voulues]
        connex.close()
        return dates, valeurs


    def obtenir_mesures_annee(self, annee, nom_table):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM %s
        """ % nom_table)

        #connex.commit() # [compteur, temperature, humidite, date]
        res = cursor.fetchall()
        mesures_voulues = [mesure for mesure in res if mesure[2].year == annee]
        valeurs = [mesure[1] for mesure in mesures_voulues]
        dates = [mesure[2] for mesure in mesures_voulues]
        connex.close()
        return dates, valeurs

    def enregistrer_mesure(self, valeur, nom_table):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        #cursor = connex.cursor()
        connex.execute("""
            INSERT INTO """+nom_table+"""(mesure, date_heure)
            VALUES (?,?);
            """, (valeur, datetime.datetime.now()))
        connex.commit()
        connex.close()

        #obtenir dernier

    def obtenir_dernier(self, nom_table):
        connex = sqlite3.connect(self.chemin_base_donnee, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM %s
        WHERE compteur IN (SELECT max(compteur) FROM %s)
        """ % (nom_table, nom_table))
        res = cursor.fetchone()
        connex.close()
        print(res)
        return res[1], res[2]



if __name__ == "__main__":
    a = RecuperateurDonnees()
    # a.creer_table()
    #print(a.obtenir_dernier("TEMPERATURE_EXTERIEURE"))
    for i in noms_tables_capteurs:
        print(i, a.obtenir_dernier(i))
    #print(a.obtenir_mesures_jour(2017, 9, 26,"TEMPERATURE_EXTERIEURE"))
    #print(a.obtenir_mesures_jour(2017, 9, 26,"HUMIDITE_AIR_EXTERIEUR"))
    #print(a.obtenir_mesures_jour(2017, 9, 26,"LUMINOSITE_EXTERIEUR"))
