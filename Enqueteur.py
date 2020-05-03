from Infobox import get_all_infobox, begin_research_infobox
from Text import get_all_text, get_victims, get_places, get_dates, get_precise_infos, get_text


# Renvoie une liste contenant des listes d'informations sur les tueurs, les listes sont au format nom du tueur,
# victimes, lieux, date début, date fin, [dates seules], (duo info: nom, date)
def get_everyone():
    infoboxes = get_all_infobox()
    all_text = get_all_text(True)

    nb_full = 0
    nb_partly_completed = 0

    enqueteur = []

    for infobox in infoboxes:
        infos = begin_research_infobox(infobox[1])
        enqueteur.append(infos)

    for i, text in enumerate(all_text):
        victims = get_victims(text)
        places = get_places(text)
        dates = get_dates(text)
        infos = get_precise_infos(text)
        if len(enqueteur[i][0]) == 0:
            enqueteur[i][0].append(text[0])
        if len(victims) > 0 and victims != None:
            enqueteur[i][1].append(victims)
        if len(places) > 0 and places != None:
            enqueteur[i][2].append(places)
        if len(dates) > 0 and dates != None:
            enqueteur[i][5].append(dates)
        if len(infos) > 0 and infos != None:
            enqueteur[i][6].append(infos)

    for killer in enqueteur:
       show_killer_infos(killer)

    return enqueteur


# Renvoie une liste contenant des informations sur un tueur (le n-ième du corpus), la liste est au format nom du
# tueur, victimes, lieux, date début, date fin, [dates seules], (duo info: nom, date)
def get_killer_number(killer_num):
    infobox, text = get_text(killer_num, True)
    # Infos de l'infobox
    enqueteur = begin_research_infobox(infobox[1])
    # Cherche les infos dans le texte
    victims = get_victims(text)
    places = get_places(text)
    dates = get_dates(text)
    infos = get_precise_infos(text)
    # Range les infos dans l'enqueteur
    if len(enqueteur[0]) == 0:
        enqueteur[0].append(text[0])
    if len(victims) > 0 and victims is not None:
        enqueteur[1].append(victims)
    if len(places) > 0 and places is not None:
        enqueteur[2].append(places)
    if len(dates) > 0 and dates is not None:
        enqueteur[5].append(dates)
    if len(infos) > 0 and infos is not None:
        enqueteur[6].append(infos)
    return enqueteur


#Permet d'afficher les infos d'un assassin précis
def show_killer_infos(killer):
    assassin = killer[0][0]
    if not (killer[1]):
        victime = "inconnu"
    else:
        victime = killer[1][0]
    if not (killer[2]):
        lieux = "inconnu"
    else:
        lieux = killer[2][0]
    if not (killer[3]):
        dateDeb = "inconnue"
    else:
        dateDeb = killer[3][0]
    if not (killer[4]):
        dateFin = "inconnue"
    else:
        dateFin = killer[4][0]
    if not (killer[6]):
        infos = "Pas d'autres infos"
    else:
        infos = killer[6][0]
    print("Assassin:", assassin, "\n Victimes:", victime, "\n Lieux des crimes:", lieux, "\n dates de début et fin:",
          dateDeb, " à ", dateFin, "\n Autres infos:", infos)

#Permet de choisir l'assassin que nous voulons étudier
def get_one_killer():
    print("Vous avez choisi de consulter le profil d'un seul tueur ! "
       "\n Ceux-ci sont numérotés de 0 à 57, veuillez entrer le numéro du tueur dont vous désirez connaître les caractéristiques")
    num = input()
    if int(num) > 57 or 0 > int(num):
        print("Veuillez entrer un numéro entre 0 et 57")
        get_one_killer()
    killer = get_killer_number(int(num))
    show_killer_infos(killer)

#Permet de choisir si on veut voir tous les assassins ou en choisir un précisement
def choose_function():
    print("Bonjour monsieur l'inspecteur, que désirez-vous faire ? Je vous propose de :"
       "\n 1. Consulter la liste exhaustive de tous les tueurs"
       "\n 2. Rechercher directement le tueur que vous souhaitez à l'aide de son numéro")
    num = input()
    if int(num) == 1:
        get_everyone()
    elif int(num) == 2:
        get_one_killer()
    else:
        print("Désolé le numéro composé n'est pas attribué")
        choose_function()


choose_function()