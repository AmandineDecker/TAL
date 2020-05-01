import collections
from lxml import etree
import re


#  nettoie l'arbre pour le rendre utilisable
def strip_ns_prefix(tree):
    # xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    # for each element returned by the above xpath query...
    for element in tree.xpath(query):
        # replace element name with its local name
        element.tag = etree.QName(element).localname
    return tree


#  nettoie l'arbre et affiche les tags de l'arbre
def clean_and_display(tree, with_namespace, display):
    if not with_namespace:  # removes namespaces
        tree = strip_ns_prefix(tree)

    nice_tree = collections.OrderedDict()

    for tag in tree.iter():  # get tags
        path = re.sub('\[[0-9]+\]', '', tree.getpath(tag))
        if path not in nice_tree:
            nice_tree[path] = []
        if len(tag.keys()) > 0:
            nice_tree[path].extend(attrib for attrib in tag.keys() if attrib not in nice_tree[path])
    if display:
        for path, attribs in nice_tree.items():  # print with indent
            indent = int(path.count('/') - 1)
            print('{0}{1}: {2} [{3}]'.format('    ' * indent, indent, path.split('/')[-1],
                                             ', '.join(attribs) if len(attribs) > 0 else '-'))


# crée une liste de tuples (nom, texte) où nom est le nom du tueur et texte l'enseble du texte de la page associée
def make_killer_list():
    wiki_tree = etree.parse('Wikipedia_Corpus.xml')
    clean_and_display(wiki_tree, False, False)

    # print("\n\n**************************************************\n")
    killers_list = []
    for user_id in range(len(wiki_tree.xpath("/mediawiki/page"))):
        name = wiki_tree.xpath("/mediawiki/page/title")[user_id].text
        txt = wiki_tree.xpath("/mediawiki/page/revision/text")[user_id].text
        killer = (name, txt)
        killers_list.append(killer)
    return killers_list


killer_list = make_killer_list()


# renvoie la position du texte (début, fin) contenu entre les accolades après beginning dans txt
def get_text_between_brackets(beginning, txt):
    if beginning not in txt:
        return (0, 0)
    else:
        index_beginning_txt = txt.index(beginning)
        i_min = -1
        i_course = index_beginning_txt - 1
        while i_min == -1:
            if txt[i_course] == '{' and txt[i_course - 1] == '{':
                i_min = i_course - 1
            else:
                i_course -= 1
    total_bracket = 2
    i_max = i_min + 2
    while total_bracket > 0 and i_max < len(txt):
        if txt[i_max] == '{':
            total_bracket += 1
        elif txt[i_max] == '}':
            total_bracket -= 1
        i_max += 1
    return i_min, i_max


# renvoie la position du texte (début, fin) utile, i.e. avant les notes/informations en bas de page
def get_text_before_see_also(txt, indice_debut):
    indice_fin = -1
    if '==See also==' in txt[indice_debut:]:
        indice_fin = txt.index('==See also==')
    elif '== See also ==' in txt[indice_debut:]:
        indice_fin = txt.index('== See also ==')
    elif '==Notes==' in txt[indice_debut:]:
        indice_fin = txt.index('==Notes==')
    elif '== Notes ==' in txt[indice_debut:]:
        indice_fin = txt.index('== Notes ==')
    elif '== Literature ==' in txt[indice_debut:]:
        indice_fin = txt.index('== Literature ==')
    elif '==References==' in txt[indice_debut:]:
        indice_fin = txt.index('==References==')
    elif '== References ==' in txt[indice_debut:]:
        indice_fin = txt.index('== References ==')
    elif '==External links==' in txt[indice_debut:]:
        indice_fin = txt.index('==External links==')
    elif '== External links ==' in txt[indice_debut:]:
        indice_fin = txt.index('== External links ==')
    elif '==Citations==' in txt[indice_debut:]:
        indice_fin = txt.index('==Citations==')
    else:
        indice_fin = -1
    if indice_fin > -1:
        return indice_debut, indice_fin
    else:
        return indice_debut, -1


# renvoie le tuple (infobox, texte) correspondant à txt, texte est le texte utile à l'enquêteur
def get_usefull_text(txt):
    if '#REDIRECT' in txt:
        return "", ""
    elif 'Infobox serial killer' in txt:
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox serial killer", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
    elif 'Infobox murderer' in txt:
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox murderer", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
    elif 'Infobox person' in txt or 'Infobox Person' in txt:
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox person", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
    elif 'Infobox criminal' in txt:
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox criminal", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
    elif 'Infobox officeholder' in txt:
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox officeholder", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
    elif 'Infobox' in txt:
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
    else:
        (infobox_begin, infobox_end) = (0, 0)
        (txt_begin, txt_end) = get_text_before_see_also(txt, 0)
    return txt[infobox_begin:infobox_end], txt[txt_begin:txt_end]


def remove_refs(txt):  # Retire ref /ref et ce qu'il y a entre
    return re.sub(r'ref.*?/ref', '', txt, flags=re.DOTALL)


def remove_ref_name(txt):  # Retire <ref name = ...>  (< = &lt; et > = &gt;)
    txt = re.sub('&lt;ref name=.*?&gt;', '', txt, flags=re.MULTILINE)
    return re.sub(r'<ref name=.*?>', '', txt, flags=re.MULTILINE)


def remove_reflist(txt):  # Retire {{Reflist}} et ce qu'il y a après
    return re.sub(r'{{Reflist}}.*', '', txt, flags=re.MULTILINE)


def remove_quotes(txt):  # Retire {{quote ...}
    txt = re.sub(r'{{quote.*?}}', '', txt, flags=re.DOTALL)
    return re.sub(r'{{Quote.*?}}', '', txt, flags=re.DOTALL)


def remove_see_also(txt):  # Retire {{See also ...?}}
    return re.sub(r'{{See also.*?}}', '', txt, flags=re.DOTALL)


def remove_files(txt):  # Retire File:.***.jpg.\n
    return re.sub(r'File:.*?.jpg.*?\n', '', txt, flags=re.DOTALL)


def remove_star_list(txt):  # Retire les listes de *
    return re.sub(r'<\*.*?\n>*', '', txt, flags=re.DOTALL)


def remove_repeats(txt):  # Remplace [[A|B]] par A
    return re.sub(r'\[\[(?P<name>.*?)\|.*?\]\]', r'\1', txt, flags=re.DOTALL)


def remove_brackets(txt):  # Remplace {{(?P<Texte>.*?)}} par Texte
    return re.sub(r'{{(?P<name>.*?)}}', r'\1', txt, flags=re.DOTALL)


def remove_specials(txt):  # Retire des caractères spéciaux (&lt; = < et &gt; = >)
    txt = re.sub("\[|\]|<>|<|>|\'+|&nbsp;|&lt;|&gt;|", '', txt, flags=re.MULTILINE)
    return txt


def remove_titels(txt):  # Retire les titres des différentes parties de la page
    txt = re.sub(r'==*.*?==*', '', txt, flags=re.DOTALL)
    return txt


def clean_text(txt):  # Nettoie le texte
    text = remove_refs(txt)
    text = remove_ref_name(text)
    text = remove_reflist(text)
    text = remove_quotes(text)
    text = remove_see_also(text)
    text = remove_files(text)
    text = remove_star_list(text)
    text = remove_repeats(text)
    text = remove_brackets(text)
    text = remove_specials(text)
    text = remove_titels(text)
    return text