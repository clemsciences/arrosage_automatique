# -*-coding:utf-8-*-
__author__ = 'Clément'

from serial import Serial, SerialTimeoutException, SerialException
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrosage_automatique.settings")
from gestion_temps import *
import threading
import sqlite3
from gestion_arrosage_automatique.models import *
import re
# port_serie = Serial(port = PORT, baudrate = 9600)

def trouver_ports_libres():
    available = []
    for i in range(256):
        try:
            s = Serial(i)
            available.append((i, s.portstr))
            s.close()
        except:
            continue
    print available


class RecuperateurDonnees:
    def __init__(self, chemin_base_donnee):
        assert isinstance(chemin_base_donnee, str)
        self.chemin_base_donnee = chemin_base_donnee

    def obtenir_conditions_meteorologiques(self):
        """
        Connexion à la base de données pour obtenir les derniers relevés de la situation météorologique
        :return:
        """

        connex = sqlite3.connect(self.chemin_base_donnee)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM ConditionsMeteorologiques
        WHERE compteur IN  (SELECT max(compteur) FROM ConditionsMeteorologiques)
        """)

        connex.commit()
        [compteur, date, temperature, humidite] = cursor.fetchone()
        res = cursor.fetchone()
        connex.close()

    def enregistrer_arrosage(self, duree):
        """
        Remplit la table Arrosage à chaque fin d'arrosage
        :param duree : durée de l'arrosage
        :return:
        """
        connex = sqlite3.connect(self.chemin_base_donnee)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT compteur
        FROM Arrosage
        WHERE compteur IN (SELECT max(compteur) FROM Arrosage)
        """)
        connex.commit()
        compteur = cursor.fetchone()
        cursor.execute("""
            INSERT INTO Arrosage(compteur, date_exacte, duree)
            VALUES (?,?,?);
            """, (str(compteur + 1), time.asctime(time.time()), str(duree)))
        connex.close()

    def obtenir_conditions_arrosage(self):
        """
        Consulte la base de donnée base_arrosage.db pour récupérer les données sur les
        moment adéquat pour arroser
        :return:
        """
        connex = sqlite3.connect(self.chemin_base_donnee)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT *
        FROM ConditionArrosage
        WHERE compteur IN (SELECT max(compteur) FROM ConditionArrosage)
        """)

        connex.commit()
        # [compteur, temperature_min, humidite_max, frequence_min, heure_min, heure_max, duree ] = cursor.fetchone()
        res = cursor.fetchone()
        connex.close()
        return res

    def enregistrer_temperature(self, date_exacte, temperature, humidite):
        # fonction quasiment identique à enregistrer_humidite
        connex = sqlite3.connect("base_arrosage.db")
        cursor = connex.cursor()
        cursor.execute("""
        SELECT compteur
        FROM ConditionsMeteorologiques
        WHERE compteur IN (SELECT max(compteur) FROM ConditionsMeteorologiques)
        """)

        connex.commit()
        compteur = cursor.fetchone()
        connex.execute("""
         INSERT INTO ConditionsMeteorologiques(compteur, date_exacte, temperature, humidite_relative)
          VALUES (?,?,?);
           """, (str(compteur + 1), time.asctime(date_exacte), str(temperature), str(humidite)))
        connex.close()

    def enregistrer_humidite(self, date_exacte, temperature, humidite):
        connex = sqlite3.connect("base_arrosage.db")
        cursor = connex.cursor()
        cursor.execute("""
        SELECT id
        FROM ConditionsMeteorologiques
        WHERE id IN (SELECT max(id) FROM ConditionsMeteorologiques)
        """)

        connex.commit()
        compteur = cursor.fetchone()
        cursor.execute("""
             INSERT INTO ConditionsMeteorologiques(id, date_exacte, temperature, humidite_relative)
            VALUES (?,?,?);
            """, (str(id + 1), time.asctime(date_exacte), str(temperature), str(humidite) ))
        connex.close()

    def enregistrer_mesure(self, date_exacte, temperature, humidite):
        connex = sqlite3.connect(self.chemin_base_donnee)
        cursor = connex.cursor()
        cursor.execute("""
        SELECT id
        FROM ConditionsMeteorologiques
        WHERE id IN (SELECT max(id) FROM ConditionsMeteorologiques)
        """)
        connex.commit()
        compteur = cursor.fetchone()
        cursor.execute("""
            INSERT INTO ConditionsMeteorologiques(id, date_exacte, temperature, humidite_relative)
            VALUES (?,?,?);
            """, (str(compteur + 1), time.asctime(date_exacte), str(temperature), str(humidite) ))
        connex.close()


class Decideur(threading.Thread):
    def __init__(self, lePort):
        threading.Thread.__init__(self)
        self.commu = Communication_Arduino(lePort)
    def run(self):
        """
        Méthode principale, là où tout se passe.
        :return:
        """
        derniere_mise_a_jour = time.time()
        derniere_prise_mesure = time.time()
        temps_dernier_arrosage = 0

        en_train_d_arroser = False
        debut_reelle_arrosage = False

        derniere_condo_meteo = ConditionsMeteorologiques.objects.get(
            id=max([i.id for i in ConditionsMeteorologiques.objects.all()]))
        print derniere_condo_meteo
        temperature = derniere_condo_meteo.temperature
        humidite = derniere_condo_meteo.humidite_relative

        derniere_condo_arrosage = ConditionArrosage.objects.get(id=max([i.id for i in ConditionArrosage.objects.all()]))
        print derniere_condo_arrosage
        temperature_min = derniere_condo_arrosage.temperature_min
        humidite_max = derniere_condo_arrosage.humidite_max
        frequence_min = derniere_condo_arrosage.frequence_min
        heure_min = derniere_condo_arrosage.heure_min
        heure_max = derniere_condo_arrosage.heure_max
        duree_arrosage_prevue = derniere_condo_arrosage.duree

        while True:
            #print 'on vérifie'
            try:
                maintenant = time.time()
                # mise à jour des données toutes les 5 minutes
                """
                if distance_seconde(maintenant, derniere_mise_a_jour) > 300:
                    print "on fait la mise à jour des paramètres d'arrosage"
                    #se tient à jour des paramètres pour arroser
                    derniere_condo_arrosage = ConditionArrosage.objects.get(
                        id=max([i.id for i in ConditionArrosage.objects.all()]))
                    temperature_min = derniere_condo_arrosage.temperature_min
                    humidite_max = derniere_condo_arrosage.humidite_max
                    frequence_min = derniere_condo_arrosage.frequence_min
                    heure_min = derniere_condo_arrosage.heure_min
                    heure_max = derniere_condo_arrosage.heure_max
                    duree_arrosage_prevue = derniere_condo_arrosage.duree
                    derniere_mise_a_jour = maintenant

                if humidite < humidite_max and distance_jour(maintenant, temps_dernier_arrosage) > \
                        frequence_min and donner_heure(maintenant) > heure_min and donner_heure(maintenant) < heure_max:
                    #vérifie si les conditions pour arroser sont remplies, si oui, on arrose
                    print "on arrose"
                    self.commu.arroser()

                    temps_dernier_arrosage = time.time()
                    lu = self.commu.ecouter()
                    if lu == "pompe_allumee":
                        debut_reelle_arrosage = maintenant
                        en_train_d_arroser = True
                if distance_seconde(maintenant, debut_reelle_arrosage) > duree_arrosage_prevue and en_train_d_arroser:
                    print "on n'arrose plus"
                    #si la durée de l'arrosage est supérieure à la durée prévue, alors on éteint la pompe
                    self.commu.eteindre_arrosage()
                    lu = self.commu.ecouter()
                    if lu == "pompe_eteinte":
                        fin_reelle_arrosage = maintenant
                        en_train_d_arroser = False
                        duree_reelle_arrosage = distance_seconde(debut_reelle_arrosage, fin_reelle_arrosage)
                        Arrosage(duree=duree_reelle_arrosage).save()
                """
                #print distance_seconde(maintenant, derniere_prise_mesure)
                if distance_seconde(maintenant, derniere_prise_mesure) > 60:
                    #demande la température et l'enregistre dans une base de donnée
                    self.commu.combien_temperature()
                    print "on mesure la température"
                    time.sleep(1)
                    lu = self.commu.ecouter()
                    print lu
                    if re.match(r"[0-9].\.[0-9].", lu) is not None:
                        temperature = lu
                        print temperature
                    else:
                        print "mauvaise donnée"
                        temperature = 0
                        continue
                    self.commu.combien_humidite()
                    print "on mesure l'humidité"
                    time.sleep(1)
                    lu = self.commu.ecouter()
                    print lu
                    if re.match(r"[0-9].\.[0-9].", lu) is not None:
                        humidite = lu
                        print humidite
                    else:
                        print "mauvaise donnée humidité"
                        humidite = 0
                        continue
                    ConditionsMeteorologiques(temperature=temperature, humidite_relative=humidite).save()
                    #self.enregistrer_mesure(maintenant, temperature, humidite)
                    derniere_prise_mesure = maintenant
                time.sleep(0.5)
            except SerialException:
                print "impossible d'accéder au port"
                break
            """
            except:
                print "rien du tout"
                self.commu.quitter()
                break
                """


class Communication_Arduino:
    def __init__(self, lePort):
        self.port = lePort
        try:
            self.port_serie = Serial(port=self.port, baudrate=9600, timeout=0)
            print self.port_serie.isOpen()
        except SerialException:
            print "impossible d'ouvrir le port : " + str(lePort)

    def combien_temperature(self):
        # combien_temperature
        self.port_serie.write("t")

    def combien_humidite(self):
        # combien_humidite
        self.port_serie.write("h")

    def arroser(self):
        # arroser
        self.port_serie.write("a")

    def eteindre_arrosage(self):
        # eteindre_arrosage
        self.port_serie.write("e")

    # def en_train_d_arroser(self):
    # self.port_serie.write("en_train_d_arroser")
    def ecouter(self):
        print "on lit"
        return self.port_serie.readline()

    def parler(self, a_envoyer):
        #raw_input("écrire ici")
        self.port_serie.write(a_envoyer)
        return a_envoyer

    def quitter(self):
        self.port_serie.close()

if __name__ == "__main__":
    PORT = "COM4"
    import os
    Decideur(PORT).run()