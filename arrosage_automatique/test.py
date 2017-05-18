# -*-coding:utf-8-*-


from arrosage_database_manager import RecuperateurDonnees
recuperateur = RecuperateurDonnees()
annee = 2017
mois = 5
temps, humidites = recuperateur.obtenir_humidite_mois(annee, mois)
print("humidité")
print(len(temps))

print(len(humidites))
temps, temperatures = recuperateur.obtenir_temprature_mois(annee, mois)
print("temperature")
print(len(temps))

print(len(temperatures))
