# -*-coding:utf-8-*-

__author__ = 'Clément'
import time




def distance_jour(t1, t2):
    """
    :param t1: vaut time.time()
    :param t2: vaut time.time()
    :return:
    """
    return abs(t2-t1) / 86400

def donner_heure(temps):
    return int(temps /3600) % 24 + 2
def distance_seconde(t1,t2):
    return abs(t2-t1)




def calculer_duree(h1,m1,s1,ms1,h2,m2,s2,ms2):
    """
    Calcule la durÃ©e en secondes entre le temps t1 et t2
    """
    duree = 0.001*((int(ms2)-int(ms1))%1000)
    if int(ms2)-int(ms1)<0:
        duree -= 1
    duree += ((int(s2)-int(s1))%60)
    if int(s2)-int(s1) <0:
        duree -= 60
    duree +=((int(m2)-int(m1))%60)*60
    if int(m2)-int(m1)<0:
        duree -= 3600
    duree += ((int(h2)-int(h1))%24)*3600
    if int(h2)-int(h1) <0:
        duree -= 86400
    return float(duree)