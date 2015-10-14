from xml.etree import ElementTree
from datetime import datetime
#tree = etree.parse("nom_fichier.xml")

def generer_ordre(categorie, **args):
    ordre = ElementTree.Element("ordre")
    ca = ElementTree.SubElement(ordre, categorie)
    for i in args.keys():
       feuille = ElementTree.SubElement(ca, i)
       feuille.text = args[i]
    return ordre



def generer_question(date, categorie, questions = None):
    if questions is None:
        questions = ElementTree.Element("questions")
    else:
        question = ElementTree.SubElement(questions, "question")
        da = ElementTree.SubElement(question, "date")
        da.text = date
        ca = ElementTree.SubElement(question, "categorie")
        ca.text = categorie
    return questions


if __name__ == "__main__":
    questions = generer_question(str(datetime.today()), "temperature")
    questions = generer_question(str(datetime.today()), "humidite", questions)
    questions = generer_question(str(datetime.today()), "parametres", questions)
    questions = generer_question(str(datetime.today()), "pression", questions)
    print(ElementTree.tostring(questions))



    ordre = generer_ordre("parametrage", periode="2", duree="7", a_partir_de="19")
    print ElementTree.tostring(ordre)
    ordre2 = generer_ordre("arroser", quand="maintenant")
    print ElementTree.tostring(ordre2)
