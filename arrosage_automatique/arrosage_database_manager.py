 # -*-coding:utf-8-*-
from sqlite3 import *
"""
Module à améliorer pour faire mieux correspondre les tables aux besoins
"""
def creer_table():
	conn = sqlite3.connect("arrosage_database.db")
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
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS ARROSAGE(
	compteur INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	date_heure timestamp)
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


