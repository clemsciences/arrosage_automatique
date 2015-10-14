# -*-coding:utf-8-*-


__author__ = 'Clément'


import smtplib

from email.mime.text import MIMEText

def envoyer_courriel(nom_fichier, objet, emetteur, recepteur):
    fichier = open(nomfichier, "r")
    courriel = MIMEText(fichier.read())
    fichier.close()
    courriel['Subject'] = objet
    courriel["From"] = emetteur
    courriel['To'] = recepteur
    smtpserveur = smtplib.SMTP()
    smtpserveur.sendmail(emetteur, recepteur, courriel, )