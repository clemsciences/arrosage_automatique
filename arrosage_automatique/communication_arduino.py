# -*-coding:utf-8-*-
__author__ = 'spraakforskaren'

import argparse
import os
import platform
import re
import sqlite3
import threading
from gestion_courriel.Gmail import *
from gestion_courriel.extraire_xml import extraire_question, extraire_ordre
from oauth2client.tools import argparser
from serial import Serial, SerialException
from arrosage_database_manager import RecuperateurDonnees

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arrosage_automatique.settings")
#import django
#django.setup()
from gestion_temps import *
#from gestion_arrosage_automatique.models import ConditionsMeteorologiques, ConditionArrosage


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


class GestionnaireGmail(threading.Thread):
    def __init__(self, json_file, PROVENANCE_SURE, DESTINATAIRES):
        print "on gère les courriels"
        threading.Thread.__init__(self)
        parser = argparse.ArgumentParser(parents=[argparser])
        self.flags = parser.parse_args()
        self.PROVENANCE_SURE = PROVENANCE_SURE
        self.json_file = json_file
        self.parser = argparse.ArgumentParser(parents=[argparser])
        self.gmail_lire = Gmail(self.flags, client_secret_file =self.json_file, oauth_scope = 'https://www.googleapis.com/auth/gmail.readonly')
        messages = self.gmail_lire.getMessagesList()
        if messages['messages']:
            self.l_id_courriels = [ msg['id'] for msg in messages['messages']]
            #= gmail.getMessageDetails(msg['id'])
        self.destinataires = DESTINATAIRES
        systeme = platform.system()
        self.rec = RecuperateurDonnees(os.getcwd())
        print "initialisation"
        self.gmail_envoyer = Gmail(self.flags, client_secret_file =self.json_file, oauth_scope = 'https://www.googleapis.com/auth/gmail.send')
        texte = """
                Bonjour\n\nLe service d'arrosage automatique a redémarré.\n\nCordialement\n\n Clément Besnier
                """
        message = Message(sender="clemsciences@gmail.com",to="clemsciences@gmail.com",subject="rapport météo",
                                                 message_text= texte, service=self.gmail_envoyer.gmail_service)
                    #message = Message_Attachment(sender="arrosage.b@gmail.com",to=destinataire,subject="rapport météo",
                    #                             message_text= "test", file_dir=os.getcwd(), filename= "",
                    #                             service=gmail.gmail_service)
        message.sendMessage(self.gmail_envoyer.gmail_service, "clemsciences@gmail.com")
    def run(self):
        derniere_mise_a_jour = time.time()
        periode_mise_a_jour_gmail = 120
        six_jours = 518400
        trois_jours = 3*24*3600
        reinitialisation_gmail = time.time()
        #maintenant = 0 #permet d'envoyer un message de démarrage
        while True:

            maintenant = time.time()
            if distance_seconde(maintenant,derniere_mise_a_jour) > periode_mise_a_jour_gmail:
                print "on vérifie les courriels reçus"
                messages = self.gmail_lire.getMessagesList()
                if messages['messages']:
                    l_id = [msg['id'] for msg in messages['messages'] if not msg['id'] in self.l_id_courriels ]
                    for msg_id in l_id:
                        m = self.gmail_lire.getMessageDetails(msg_id)
                        if m.getFrom() in self.PROVENANCE_SURE:
                            self.rec.enregistrer_courriel(self, m.getFrom(), m.getTo(), m.getSubject(), m.getText(self.gmail_lire.gmail_service, 'me', msg_id))
                            if m.getSubject() == "ordre":
                                l_instructions = extraire_ordre(m.getText(self.gmail_lire.gmail_service,"clemsciences@gmail.com", msg_id))
                                # for instruction in l_instructions:
                                #     if instruction['categorie']
                                #     RecuperateurDonnees.obtenir_conditions_meteorologiques()
                            elif m.getSubject() == "questions":
                                l_instructions = extraire_question(m.getText(self.gmail_lire.gmail_service, "clemsciences@gmail.com", msg_id))
                            else:
                                pass
                            if m.getSubject() == "IP":
                                self.gmail_envoyer = Gmail(self.flags, client_secret_file =self.json_file, oauth_scope = 'https://www.googleapis.com/auth/gmail.send')
                                #ip = os.system("ifconfig")
                                message = Message(sender="clemsciences@gmail.com",to="clemsciences@gmail.com",subject="IP",
                                                 message_text= "faut m'extraire", service=self.gmail_envoyer.gmail_service)
                                message.sendMessage(self.gmail_envoyer.gmail_service, "clemsciences@gmail.com")
                                self.gmail_lire = Gmail(self.flags, client_secret_file =self.json_file, oauth_scope = 'https://www.googleapis.com/auth/gmail.readonly')


                derniere_mise_a_jour = maintenant
            elif distance_jour(maintenant, reinitialisation_gmail) > 6:
                print "on réinitialise la connexion"
                self.gmail_lire = Gmail(self.flags, client_secret_file = self.json_file, oauth_scope = 'https://www.googleapis.com/auth/gmail.readonly')
                self.gmail_envoyer = Gmail(self.flags, client_secret_file = self.json_file, oauth_scope = 'https://www.googleapis.com/auth/gmail.send')
                reinitialisation_gmail = maintenant
            elif distance_jour(maintenant, reinitialisation_gmail) > 3:
                print "on envoie un courriel à tout le monde"
                for destinataire in self.destinataires:

                    print self.rec.obtenir_conditions_meteorologiques()
                    #res = [(i.temperature,i.humidite_relative, i.date) for i in ConditionsMeteorologiques.objects.all() if datetime.timedelta.total_seconds(i.date - datetime.datetime.now())]
                    self.rec.obtenir_conditions_meteorologiques_depuis(3)
                    message = Message_Attachment(sender="clemsciences@gmail.com",to="clemsciences@gmail.com",subject="rapport météo",
                                                 message_text= "test", service=self.gmail_envoyer.gmail_service)
                    #message = Message_Attachment(sender="arrosage.b@gmail.com",to=destinataire,subject="rapport météo",
                    #                             message_text= "test", file_dir=os.getcwd(), filename= "",
                    #                             service=gmail.gmail_service)
                    message.sendMessage(self.gmail_envoyer.gmail_service, "clemsciences@gmail.com")



class Decideur(threading.Thread):
    def __init__(self, lePort):
        threading.Thread.__init__(self)
        self.commu = Communication_Arduino(lePort)
        self.recuperateur = RecuperateurDonnees("base_arrosage.db")
    def run(self):
        """
        Méthode principale, là où tout se passe.
        :return:
        """
        print "on mesure aussi !"
        derniere_mise_a_jour = time.time()
        derniere_prise_mesure = time.time()
        temps_dernier_arrosage = 0

        en_train_d_arroser = False
        debut_reelle_arrosage = False

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

                print distance_seconde(maintenant, derniere_prise_mesure)
                if distance_seconde(maintenant, derniere_prise_mesure) > 180:
                    #demande la température et l'enregistre dans une base de donnée
                    self.commu.combien_temperature()
                    print "on mesure la température"
                    time.sleep(1)
                    lu = self.commu.ecouter()
                    print lu
                    if re.match(r"(RX : )[0-9].\.[0-9].", lu) is not None:
                        temperature = lu[5:] #TODO à remettre sans RX :
                        print temperature
                    elif re.match(r"[0-9].\.[0-9].", lu):
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
                    if re.match(r"(RX : )[0-9].\.[0-9].", lu) is not None:
                        humidite = lu[5:] #TODO à remettre sans RX :
                        print humidite
                    elif re.match(r"[0-9].\.[0-9].", lu):
                        humidite = lu
                        print humidite
                    else:
                        print "mauvaise donnée humidité"
                        humidite = 0
                        continue
                    #on met à jour la date de dernière mesure et la dernière mesure que si on a bien eu la température
                    ## et l'humidité
                    self.recuperateur.enregistrer_mesure(temperature, humidite)#ConditionsMeteorologiques(temperature=temperature, humidite_relative=humidite).save()
                    derniere_prise_mesure = maintenant
                if distance_seconde(maintenant, derniere_prise_mesure) > 3600:
                    pass
                    #TODO problème de réception, il faut envoyer un courriel d'erreur !
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
            print "port série introuvable"

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

    if platform.system() == "Windows":
        PORT = "COM3"
    else:
        PORT = "/dev/ttyACM0"
    #try:
    dec = Decideur(PORT)
    json_file = os.path.join("gestion_courriel", "client_secret.json")
    print json_file
    PROVENANCE_SURE = ["clemsciences@gmail.com","arrosage.b@gmail.com", "cendrine.besnier37@gmail.com", "patrick.besnier37@gmail.com"]
    DESTINATAIRES = ["clemsciences@gmail.com", "patrick.besnier37@gmail.com", "cendrine.besnier37@gmail.com"]
    gest = GestionnaireGmail(json_file, PROVENANCE_SURE, DESTINATAIRES)
    #dec.start()
    gest.start()
    #except SerialException:
    #    print "port manquant"
        #TODO envoyer un mail?

