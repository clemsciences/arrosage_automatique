# -*-coding:utf-8-*-


import argparse
import os
import platform
import json
import re
import threading
import time
from gestion_courriel.Gmail import *
from gestion_courriel.extraire_xml import extraire_question, extraire_ordre
from oauth2client.tools import argparser
from serial import Serial, SerialException
from arrosage_database_manager import RecuperateurDonnees
import datetime
import collections
import numpy as np
import pickle
import generateur_graphique_meteo
from constantes import *

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrosage_automatique.settings")
#import django
#django.setup()
from gestion_temps import *
#from gestion_arrosage_automatique.models import ConditionsMeteorologiques, ConditionArrosage

__author__ = 'besnier'
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
    print(available)






class Decideur(threading.Thread):
    def __init__(self, lePort):
        threading.Thread.__init__(self)
        self.commu = Communication_Arduino(lePort)
        self.recuperateur = RecuperateurDonnees()
        self.dm = Mesure(codes_arduino)
        self.dm.initialiser_mesures()
        self.arro = Arrosage()

    def run(self):
        """
        Méthode principale, là où tout se passe.
        :return:
        """
        print("on mesure aussi !")
        date_maintenant = datetime.datetime.now()


        heure_des_mesures = datetime.datetime.now().hour
        # derniere_mise_a_jour = time.time()
        # derniere_prise_mesure_exterieure = time.time()
        # derniere_prise_mesure_interieure = time.time()
        # temps_dernier_arrosage = 0
        #
        # en_train_d_arroser = False
        # debut_reelle_arrosage = False

        # compteur, temperature, humidite, date_heure = self.recuperateur.obtenir_derniere_mesure_meteo()
        #temperature = derniere_condo_meteo.temperature
        #humidite = derniere_condo_meteo.humidite_relative

        # compteur, temperature_min, humidite_max, frequence_min, heure_min, heure_max, duree_arrosage_prevue = self.recuperateur.obtenir_conditions_arrosage() #ConditionArrosage.objects.get(id=max([i.id for i in ConditionArrosage.objects.all()]))
        #print derniere_condo_arrosage
        #temperature_min = derniere_condo_arrosage.temperature_min
        #humidite_max = derniere_condo_arrosage.humidite_max
        #frequence_min = derniere_condo_arrosage.frequence_min
        #heure_min = derniere_condo_arrosage.heure_min
        #heure_max = derniere_condo_arrosage.heure_max
        #duree_arrosage_prevue = derniere_condo_arrosage.duree

        while True:
            #print 'on vérifie'
            print("début boucle")
            try:
                # maintenant = time.time()
                date_maintenant = datetime.datetime.now()

                print(self.dm.l_grandeurs_a_mesurer)
                for code in self.dm.l_grandeurs_a_mesurer:
                    print(code)
                    self.commu.parler(code)
                    self.dm.mettre_a_jour_demandes(code)
                    time.sleep(3)
                    recu = self.commu.ecouter()
                    print(recu)
                    recu = recu.split("_")
                    if len(recu) == 2 and recu[0] in codes_capteurs:
                        code_capteur = recu[0]
                        #mesures_et_arrosages.db
                        valeur = recu[1].split("\r")[0]
                        self.dm.mettre_a_jour_receptions(code)
                        self.recuperateur.enregistrer_mesure(valeur, d_code_table_capteurs[code_capteur])
                    elif len(recu) == 0:
                        print("rien reçu")
                    else:
                        with open(os.path.join("static", "json_files", "log.json"), "a") as f:
                            json.dump({repr(datetime.datetime.now()): "truc bizarre reçu "+"_".join(recu)}, f)
                self.dm.pour_faire_nouvelles_mesures(30)
                # Voir si la carte renvoie quelque chose malgré la non réception de valeurs des capteurs
                if self.dm.non_reception[codes_capteurs.index("HS")]:
                    self.commu.demander_si_bonne_reception("beth")
                elif self.dm.non_reception[codes_capteurs.index("TE")] and dm.non_reception[codes_capteurs.index("HA")] \
                    and self.dm.non_reception[codes_capteurs.index("LU")]:
                    self.commu.demander_si_bonne_reception("gimel")

                if self.arro.verifier_si_on_arrose(5):
                    self.commu.arroser()
                if self.arro.verifier_si_on_arrete(5):
                    self.commu.eteindre_arrosage()
                time.sleep(3)




                if date_maintenant.hour != heure_des_mesures or date_maintenant.hour % 15 == 0:
                    os.system("scp mesures_et_arrosages.db blerepi@192.168.1.27:/var/www/html/BLOGS/blog_flask/mesures_et_arrosages.db")

                    # Toutes les heures, on modifie les images
                    heure_des_mesures = date_maintenant.hour
                    annee, mois, jour = date_maintenant.year, date_maintenant.month, date_maintenant.day
                    temps_te, temperatures = self.recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["TE"])
                    temps_hu, humidites = self.recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["HA"])
                    temps_pression, pressions = self.recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["PR"])
                    generateur_graphique_meteo.obtenir_courbe_global_jour(temperatures, humidites, pressions, temps_te, temps_hu, temps_pression)

                    temps_luminosite, luminosite = self.recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["LU"])
                    generateur_graphique_meteo.creer_courbe_luminosite_jour(luminosite, temps_luminosite)

                    temps_hs, humidite_sol = self.recuperateur.obtenir_mesures_jour(annee, mois, jour, d_code_table_capteurs["HS"])
                    generateur_graphique_meteo.creer_courbe_humidite_sol(humidite_sol, temps_hs)

                    # Création ou mise à jour du fichier json pour l'API REST
                    temps_moyennes_par_heure = list(set([timme.hour for timme in temps_te]))
                    temps_moyennes_par_heure.sort()
                    moyennes_par_heure_temperature = collections.defaultdict(str)
                    moyennes_par_heure_temperature.update({heure : str(float(np.mean([tempe for i, tempe in enumerate(temperatures) if temps_te[i].hour == heure and type(tempe) == float])))[:5] for heure in temps_moyennes_par_heure})

                    temps_moyennes_par_heure = list(set([timme.hour for timme in temps_hu]))
                    temps_moyennes_par_heure.sort()
                    moyennes_par_heure_humidite = collections.defaultdict(str)

                    moyennes_par_heure_humidite.update({heure : str(float(np.mean([humi for i, humi in enumerate(humidites) if temps_hu[i].hour == heure and type(humi) == float])))[:5] for heure in temps_moyennes_par_heure})

                    temps_moyennes_par_heure = list(set([timme.hour for timme in temps_pression]))
                    temps_moyennes_par_heure.sort()
                    moyennes_par_heure_pression = collections.defaultdict()
                    moyennes_par_heure_pression.update({heure: str(float(np.mean([pres for i, pres in enumerate(pressions) if temps_pression[i].hour == heure and type(pres) == float])))[:7] for heure in temps_moyennes_par_heure})

                    temps_moyennes_par_heure = list(set([timme.hour for timme in temps_hs]))
                    temps_moyennes_par_heure.sort()
                    moyennes_par_heure_hs = collections.defaultdict(str)
                    moyennes_par_heure_hs.update({heure : str(float(np.mean([hs for i, hs in enumerate(humidite_sol) if temps_hs[i].hour == heure and type(hs) == float])))[:5] for heure in temps_moyennes_par_heure})


                    temps_moyennes_par_heure = list(set([timme.hour for timme in temps_luminosite]))
                    temps_moyennes_par_heure.sort()
                    moyennes_par_heure_luminosite = collections.defaultdict(str)
                    moyennes_par_heure_luminosite.update({heure : str(float(np.mean([lumi for i, lumi in enumerate(luminosite) if temps_luminosite[i].hour == heure and type(lumi) == float])))[:5] for heure in temps_moyennes_par_heure})

                    d = {heure : {'humidite': moyennes_par_heure_humidite[heure], 'pression': moyennes_par_heure_pression[heure],"temperature": moyennes_par_heure_temperature[heure]} for heure in temps_moyennes_par_heure}
                    with open(os.path.join(DIRECTORY_JSON, nommer_jour_json("data_jour_", str(annee), str(mois), str(jour))), "wb") as f:
                        myp = pickle.Pickler(f)
                        myp.dump(d)


                time.sleep(1)
            except SerialException:
                print("impossible d'accéder au port")
                break
            """
            except:
                print "rien du tout"
                self.commu.quitter()
                break
                """


class Arrosage:
    def __init__(self, chemin=os.path.join("static", "json_files"), nom_fichier="parametres_simples_arrosage.json"):
        self.chemin = chemin
        self.nom_fichier = nom_fichier
        if os.listdir(self.chemin):
            self.creer_parametres_par_defaut()
        self.en_train_d_arroser = False
        self.charger_horaires()

    def creer_parametres_par_defaut(self):
        with open(os.path.join(self.chemin, self.nom_fichier), "w") as f:
            d = {"1": [{"heure": 6, "minute": 0}, {"heure": 6, "minute": 15}],
                "2": [{"heure": 20, "minute": 30}, {"heure": 20, "minute": 45}]}
            #  print(d)
            json.dump(d, f)

    def charger_horaires(self):
        with open(os.path.join(self.chemin, self.nom_fichier), "r") as f:
            self.horaires_d_arrosage = json.load(f)

    def verifier_si_on_arrose(self, minutes, type_arrosage="defaut"):
        if type_arrosage == "defaut":
            self.decision_temporelle_pour_demarrer(5)
            self.en_train_d_arroser = True
        else:
            return False

    def verifier_si_on_arrete(self, minutes):
        maintenant = datetime.datetime.now()
        if self.en_train_d_arroser :
            for cle in self.horaires_d_arrosage.keys():
                n = self.horaires_d_arrosage[cle]
                heure_d_arrosage = maintenant.replace(hour=n[1]["heure"], minute=n[1]["minute"])
                if moins_minute(maintenant, heure_d_arrosage, minutes):
                    return True
        return False

    def decision_temporelle_pour_demarrer(self, minutes):
        """


        :param minutes: plus ou moins ça quand on va arroser
        :return:
        """
        maintenant = datetime.datetime.now()
        #  print(self.horaires_d_arrosage)
        for cle in self.horaires_d_arrosage.keys():
            n = self.horaires_d_arrosage[cle]
            #  print(n, self.horaires_d_arrosage)
            heure_d_arrosage = maintenant.replace(hour=n[0]["heure"], minute=n[0]["minute"])
            if moins_minute(maintenant, heure_d_arrosage, minutes):
                return True
        return False


class Mesure:
    """
    Classe instanciée qu'une seule fois
    """
    def __init__(self, l_grandeurs_codee):
        self.l_grandeurs_codee = l_grandeurs_codee
        maintenant = datetime.datetime.now()
        if maintenant.minute < 59:
            
            avant = maintenant.replace(minute=maintenant.minute+1)
        else:
            avant = maintenant.replace(minute=maintenant.minute-1)
        self.dates_dernieres_demandes = [avant]*len(l_grandeurs_codee)
        self.dates_dernieres_receptions = [maintenant]*len(l_grandeurs_codee)
        self.non_reception = [False]* len(l_grandeurs_codee)
        self.l_grandeurs_a_mesurer = []

    def initialiser_mesures(self):

        self.l_grandeurs_a_mesurer = [i for i in self.l_grandeurs_codee]

    def pour_faire_nouvelles_mesures(self, intervalle_entre_mesures):
        maintenant = datetime.datetime.now()
        # print("self.l_grandeurs_codee", self.l_grandeurs_codee)
        for i in range(len(self.l_grandeurs_codee)):
            intervalle_mesuree = (self.dates_dernieres_receptions[i] - self.dates_dernieres_demandes[i])
            intervalle_attente = (maintenant - self.dates_dernieres_receptions[i])
            print(self.l_grandeurs_codee[i])
            print(intervalle_mesuree)
            print(intervalle_attente)
            if intervalle_attente.seconds > intervalle_entre_mesures and not self.non_reception[i] and self.l_grandeurs_codee[i] not in self.l_grandeurs_a_mesurer:
                self.l_grandeurs_a_mesurer.append(self.l_grandeurs_codee[i])

            elif intervalle_attente.seconds > intervalle_entre_mesures*3 and self.non_reception[i] and self.l_grandeurs_codee[i] not in self.l_grandeurs_a_mesurer:
                self.l_grandeurs_a_mesurer.append(self.l_grandeurs_codee[i])

            if - intervalle_mesuree.seconds > intervalle_entre_mesures*10:
                self.non_reception[i] = True

    def log_etat_capteurs(self):
        try:
            with open(os.path.join("static", "json_files", "log_etats_capteurs.json"), "w") as f:
                json.dump({self.l_grandeurs_codee[i]: self.non_reception[i] for i in range(len(self.l_grandeurs_codee))}, f)
        except IOError:
             with open(os.path.join("static", "json_files", "log.json"), "a") as f:
                json.dump({repr(datetime.datetime.now()): "problème avec le log de l'état des capteurs"}, f)

    def mettre_a_jour_demandes(self, code):
        self.dates_dernieres_demandes[codes_arduino.index(code)] = datetime.datetime.now()

    def mettre_a_jour_receptions(self, code):
        self.dates_dernieres_receptions[codes_arduino.index(code)] = datetime.datetime.now()
        self.l_grandeurs_a_mesurer.remove(code)


class Communication_Arduino:
    def __init__(self, lePort):
        self.port = lePort
        try:
            self.port_serie = Serial(port=self.port, baudrate=9600, timeout=0)
            print(self.port_serie.isOpen())
        except SerialException:
            print("port série introuvable")

    def combien_temperature(self):
        # combien_temperature
        self.port_serie.write("t")

    def combien_humidite(self):
        # combien_humidite
        self.port_serie.write("h")

    def combien_pression(self):
        # combien pression atmosphérique
        self.port_serie.write("p")

    def combien_temperature_interieure(self):
        self.port_serie.write("i")

    def arroser(self):
        # arroser
        self.port_serie.write("a")

    def eteindre_arrosage(self):
        # eteindre_arrosage
        self.port_serie.write("e")

    def demander_si_bonne_reception(self, nom_carte):
        if nom_carte in noms_cartes_arduino:
            if nom_carte == "beth":
                self.port_serie.write("v")
            elif nom_carte == "gimel":
                self.port_serie.write("o")
            retour = self.port_serie.readline()
            time.sleep(3)
            if retour == "connexion_bet_ok":
                self.contact_beth = True
            elif retour == "connexion_gimel_ok":
                self.contact_gimel = True
            else:
                with open(os.path.join("static", "json_files", "log.json"), "a") as f:
                    json.dump({repr(datetime.datetime.now()): "plus de contact avec la carte "+nom_carte}, f)

        else:
            with open(os.path.join("static", "json_files", "log.json"), "a") as f:
                json.dump({repr(datetime.datetime.now()): "mauvais nom de crate arduino"}, f)


    # def en_train_d_arroser(self):
    # self.port_serie.write("en_train_d_arroser")
    def ecouter(self):
        print("on lit")
        return self.port_serie.readline()

    def parler(self, a_envoyer):
        #raw_input("écrire ici")
        self.port_serie.write(a_envoyer)
        return a_envoyer

    def quitter(self):
        self.port_serie.close()



if __name__ == "__main__":

    if platform.system() == "Windows":
        PORT = "COM3"
    else:
        PORT = "/dev/ttyACM0"
    #try:
    dec = Decideur(PORT)
    #json_file = os.path.join("gestion_courriel", "client_secret.json")
    #print json_file
    #PROVENANCE_SURE = ["clemsciences@gmail.com","arrosage.b@gmail.com", "cendrine.besnier37@gmail.com", "patrick.besnier37@gmail.com"]
    #DESTINATAIRES = ["clemsciences@gmail.com", "patrick.besnier37@gmail.com", "cendrine.besnier37@gmail.com"]
    #gest = GestionnaireGmail(json_file, PROVENANCE_SURE, DESTINATAIRES)
    dec.start()
    #gest.start()
    #except SerialException:
    #    print "port manquant"
        #TODO envoyer un mail?

