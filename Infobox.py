from Preprocessing import make_killer_list, get_usefull_text
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

killer_list = make_killer_list()


def clean_infobox(infobox):
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
    return infos


def get_infobox(clean):
    infoboxes = []
    for killer in killer_list:
        infobox, text = get_usefull_text(killer[1])
        if clean:
            infoboxes.append((killer[0], clean_infobox(infobox)))
        else:
            infoboxes.append((killer, infobox))
    return infoboxes


def print_infobox(infobox, cleaned):
    if cleaned:
        print("***   " + infobox[0] + "   ***")
        print()
        for info in infobox[1:]:
            for i in info:
                print(i)
    else:
        print("***   " + infobox[0][0] + "   ***")
        print()
        print(infobox[1])
    print()
    print()


# Récupère les infoboxs, mettre True pour nettoyer le contenu, c'est plus joli mais je sais pas si ça marche à chaque fois :)
infoboxes = get_infobox(False)
# Affiche une seule infobox (mettre le même booléen que pour get_infobox)
# print_infobox(infoboxes[1], False)
# Les affiche toutes (mettre le même booléen que pour get_infobox)
#  for infobox in infoboxes:
#       print_infobox(infobox, False)


# Pour récupérer et ranger les infos utiles des infobox

lemmatizer = WordNetLemmatizer()

syn_name = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('name'))] + ['name']
# print('name: ')
# print(syn_name)
syn_victims = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('victims'))] + ['victims']
# print('victims: ')
# print(syn_victims)
syn_place = [w.lemma_names()[0] for w in
             wn.synsets(lemmatizer.lemmatize('place')) + wn.synsets(lemmatizer.lemmatize('country'))] + ['country'] + ['states']
# print('country: ')
# print(syn_place)
syn_beginyear = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('beginyear'))] + ['beginyear']
# print('beginyear: ')
# print(syn_beginyear)
syn_endyear = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('endyear'))] + ['endyear']
# print('endyear: ')
# print(syn_endyear)

def trainee_infobox_kill(infobox):
    enqueteur = [[], [], [], [], []]
    txt = infobox.replace("|", "")
    tokens = txt.split("\n")[1:]
    # print(tokens)
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
            enqueteur[0].append(info[1])
        elif info[0] in syn_victims:
            enqueteur[1].append(info[1])
        elif info[0] in syn_place:
            enqueteur[2].append(info[1])
        elif info[0] in syn_beginyear:
            enqueteur[3].append(info[1])
        elif info[0] in syn_endyear:
            enqueteur[4].append(info[1])
    # print(enqueteur)
    return enqueteur

def is_full(list):
    for x in list:
        if x == []:
            return False
    return True


infoboxes = get_infobox(False)
nb_full = 0
for infobox in infoboxes:
    print("***   " + infobox[0][0] + "   ***")
    infos = trainee_infobox_kill(infobox[1])
    if is_full(infos):
        print(infos)
        nb_full += 1
print()
print()
print('***** Nombre de listes complètes: *****')
print(nb_full)