# -*-coding:utf-8-*-


from arrosage_database_manager import RecuperateurDonnees
recuperateur = RecuperateurDonnees()
annee = "2017"
mois = "05"
temps, humidites = recuperateur.obtenir_humidite_mois(annee, mois)
print("humidité")
print(temps)

print(humidites)
temps, temperatures = recuperateur.obtenir_temprature_mois(annee, mois)
print("temperature")
print(temps)

print(temperatures)
