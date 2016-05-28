 # -*-coding:utf-8-*-
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def accueil():
	return render_template('accueil.html')

@app.route('/parametrage_arrosage/')
def parametrage_arrosage():
	return render_template("conditions_arrosages.html")

@app.route('/statistiques_meteo/')
def statistiques_meteorologique():
	return render_template("statistiques_meteo.html")

@app.route('/statistiques_arrosages/')
def statistiques_arrosage():
	return render_template("statistiques_arrosages.html")

@app.route('/rapport_courriel/')
def rapport_courriel():
	return render_template("rapport_courriel.html")

if __name__ == "__main__":
	app.run(debug=True)
