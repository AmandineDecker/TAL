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
