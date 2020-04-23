from Preprocessing import make_killer_list, get_usefull_text

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
    print("***   " + infobox[0][0] + "   ***")
    print()
    if cleaned:
        for info in infobox:
            print(info)
    else:
        print(infobox[1])
    print()
    print()


# Récupère les infoboxs, mettre True pour nettoyer le contenu, c'est plus joli mais je sais pas si ça marche à chaque fois :)
infoboxes = get_infobox(False)
# Affiche une seule infobox (mettre le même booléen que pour get_infobox)
print_infobox(infoboxes[1], False)
# Les affiche toutes (mettre le même booléen que pour get_infobox)
for infobox in infoboxes:
    print_infobox(infobox, False)