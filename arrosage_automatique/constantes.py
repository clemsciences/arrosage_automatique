# -*-coding:utf-8-*-
__author__ = 'besnier'

# code pour communiquer de la série à l'Arduino pour faire des mesures

codes_arduino = ["t", "i", "p", "h", "s","l"]
codes_capteurs = ["TE", "TI", "PR", "HA", "HS", "LU"]

noms_tables_capteurs = ["TEMPERATURE_EXTERIEURE", "TEMPERATURE_INTRIEURE", "PRESSION_ATMO", "HUMIDITE_AIR_EXTERIEUR",
                        "HUMIDITE_SOL", "LUMINOSITE_EXTERIEUR"]


d_code_table_capteurs = {code: table  for code, table in zip(codes_capteurs, noms_tables_capteurs)}


l_code_arduino_sarrosage = ["a", "e"]
l_code_arrosage = ["PA", "PE"]

noms_cartes_arduino = ["alef", "beth", "gimel", "dalet"]

# graphique humidite moyenne jour
MOHJ = "moyennes_humidite_jour_"
# graphique humidite moyenne mois
MOHM = "moyennes_humidite_mois_"
# graphique humidite moyenne annee
MOHA = "nom_humidite_annee_moyennes_"

# graphique pression moyenne jour
MOPJ = "moyennes_pression_jour_"
# graphique pression moyenne mois
MOPM = "moyennes_pression_mois_"
# graphique pression moyenne annee
MOPA = "moyennes_pression_annee_"

# graphique temperature moyenne jour
MOTJ = "moyennes_temperature_jour_"
# graphique temperature moyenne mois
MOTM = "moyennes_temperature_mois_"
# graphique temperature moyenne annee
MOTA = "nom_temperature_annee_moyennes"




# graphique humidite minima jour
MIHJ = "minima_humidite_jour_"
# graphique humidite minima mois
MIHM = "minima_humidite_mois_"
# graphique humidite minima annee
MIHA = "nom_humidite_annee_minima_"

# graphique pression minima jour
#MIPJ
# graphique pression minima mois
#MIPM
# graphique pression minima annee
#MIPA

# graphique temperature minima jour
MITJ = "minima_temperature_jour_"
# graphique temperature minima mois
MITM = "minima_temperature_mois_"
# graphique temperature minima annee
MITA = "nom_temperature_annee_minima"




# graphique humidite maxima jour
MAHJ = "maxima_humidite_jour_"
# graphique humidite maxima mois
MAHM = "maxima_humidite_mois_"
# graphique humidite maxima annee
MAHA = "nom_humidite_annee_maxima_"

# graphique pression maxima jour
#MAPJ
# graphique pression maxima mois
#MAPM
# graphique pression maxima annee
#MAPA

# graphique temperature maxima jour
MATJ = "maxima_temperature_jour_"
# graphique temperature maxima mois
MATM = "maxima_temperature_mois_"
# graphique temperature maxima annee
MATA = "nom_temperature_annee_maxima"

def nommer_jour(racine, annee, mois, jour):
    return racine+str(annee)+"_"+str(mois)+"_"+str(jour)+".png"

def nommer_mois(racine, annee, mois):
    return racine+str(annee)+"_"+str(mois)+".png"

def nommer_annee(racine, annee):
    return racine+str(annee)+".png"

def nommer_jour_json(racine, annee, mois, jour):
    return racine+str(annee)+"_"+str(mois)+"_"+str(jour)+".json"

DIRECTORY_JSON = "/home/pi/arrosage_automatique/arrosage_automatique/static/json_files"
DIRECTORY_IMAGES = "/home/pi/arrosage_automatique/arrosage_automatique/static/images"
