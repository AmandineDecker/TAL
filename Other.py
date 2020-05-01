# Nettoie un set d'informations pour éviter les doublons d'infos (date partielle et date complète par exemple)
def clean_set(set):
    a_supprimer = []
    for element in set:
        for s in set:
            if element in s and element != s:
                a_supprimer.append(element)
    for x in a_supprimer:
        set.remove(x)
    return set


# Renvoie True si toutes les listes de la liste sont non vides
def is_full(list):
    for x in list:
        if x == []:
            return False
    return True


# Renvoie True si au moins une liste de la liste est non vide
def is_partly_completed(list):
    for x in list[1:]:
        if x != []:
            return True
    return False