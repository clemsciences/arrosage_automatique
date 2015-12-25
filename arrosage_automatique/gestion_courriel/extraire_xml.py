from xml.etree import ElementTree
from datetime import datetime

#tree = etree.parse("nom_fichier.xml")

def extraire_ordre(ordre_xml):
    l = []
    for i in list(ordre_xml):
        d = {}
        for j in i.iter():
            if j.tag != "question":
                d[j.tag] = j.text
        l.append(d)
    return l

def extraire_question(questions_xml = None):
    l = []
    for i in list(questions_xml):
        d = {}
        for j in i.iter():
            if j.tag != "question":

                d[j.tag] = j.text
        l.append(d)
    return l


if __name__ == "__main__":
    from generer_xml import generer_ordre, generer_question
    questions = generer_question(str(datetime.today()), "temperature")
    questions = generer_question(str(datetime.today()), "humidite", questions)
    questions = generer_question(str(datetime.today()), "parametres", questions)
    questions = generer_question(str(datetime.today()), "pression", questions)
    print(ElementTree.tostring(questions))
    print extraire_question(questions)



    ordre = generer_ordre(type="parametrage", periode="2", duree="7", a_partir_de="19")
    print extraire_ordre(ordre)
    ordre = generer_ordre(type = "arroser", quand="maintenant")
    print extraire_ordre(ordre)