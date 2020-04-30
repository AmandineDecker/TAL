from Infobox import get_infobox, is_full, trainee_infobox_kill
from Text import get_text, get_victims, get_places, get_dates, get_precise_infos

infoboxes = get_infobox(False) # nom du tueur, victimes, lieux, date début, date fin, [dates seules], (duo info: nom, date)
all_text = get_text(True)

nb_full = 0

enqueteur = []

for infobox in infoboxes:
    infos = trainee_infobox_kill(infobox[1])
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
    if is_full(enqueteur[i][4:]):
        nb_full += 1

for killer in enqueteur:
    print(killer)


