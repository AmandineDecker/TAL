import re

from Preprocessing import make_killer_list, get_usefull_text
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


# Récupère le texte du corpus
killer_list = make_killer_list()




# Nettoie les informations
def clean_info(info):
    info = re.sub(r"""<ref name""", '', info)
    info = re.sub(r"""<small>(?P<name>.*?)</small>""", r'\1', info)
    info = re.sub(r"""<br>(?P<name>.*?)</br>""", r'\1', info)
    info = re.sub(r"""\[+(?P<name>.*?)\]+""", r'\1', info)
    info = re.sub(r"""{+(?P<name>.*?)}+""", r'\1,', info)
    info = re.sub(r"""<small>|</small>|<br>|</br>""", '', info)
    info = re.sub(r"""<br/>""", ' ', info)
    return info


# Renvoie une liste contenant toutes les infobox au format (killer, infobox)
def get_all_infobox():
    infoboxes = []
    for killer in killer_list:
        infobox, text = get_usefull_text(killer[1])
        infoboxes.append((killer, infobox))
    return infoboxes


# Pour récupérer et ranger les infos utiles des infobox

lemmatizer = WordNetLemmatizer()

syn_name = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('name'))] + ['name']
syn_victims = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('victims'))] + ['victims']
syn_place = [w.lemma_names()[0] for w in
             wn.synsets(lemmatizer.lemmatize('place')) + wn.synsets(lemmatizer.lemmatize('country'))] + ['country'] + [
                'states']


# Renvoie une liste d'informations sur le tueur, les informations sont cherchées dans l'es i'nfobox
def begin_research_infobox(infobox):
    enqueteur = [[], [], [], [], [], [],
                 []]  # nom du tueur, victimes, lieux, date début, date fin, [dates seules], (duo info: nom, date)
    txt = infobox.replace("|", "")
    tokens = txt.split("\n")[1:]
    infos = []
    for t in tokens:
        if '=' in t:
            if t[0] == " ":
                t = t[1:]
            info = t.split('=')
            # print(info)
            if info[1] != "" and info[1] != " " and info[1 != "\n"]:
                info[0] = info[0].strip()
                info[1] = info[1].strip()
                infos.append((info))
    for info in infos:
        if info[0] in syn_name:
            enqueteur[0].append(clean_info(info[1]))
        elif info[0] in syn_victims:
            enqueteur[1].append(clean_info(info[1]))
        elif info[0] in syn_place:
            enqueteur[2].append(clean_info(info[1]))
        elif info[0] == 'beginyear':
            enqueteur[3].append(clean_info(info[1]))
        elif info[0] == 'endyear':
            enqueteur[4].append(clean_info(info[1]))
    return enqueteur
