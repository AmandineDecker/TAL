import re, collections
from lxml import etree


#  change tree in URL ???

#  remove namespace (http://www.mediawiki.org/xml/export-0.10/ by us), enables easy tree traversal
def strip_ns_prefix(tree):
    # xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    # for each element returned by the above xpath query...
    for element in tree.xpath(query):
        # replace element name with its local name
        element.tag = etree.QName(element).localname
    return tree


#  remove namespaces and display tags ef the tree
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

def get_text_between_brackets(beginning, txt):
    if beginning not in txt:
        print("Text not found")
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


def get_text_before_see_also(txt, indice_debut):
    if '==See also==' in txt[indice_debut:]:
        indice_fin = txt.index('==See also==')
    elif '==Notes==' in txt[indice_debut:]:
        indice_fin = txt.index('==Notes==')
    elif '==References==' in txt[indice_debut:]:
        indice_fin = txt.index('==References==')
    elif '==External links==' in txt[indice_debut:]:
        indice_fin = txt.index('==External links==')
    else:
        indice_fin = -1
    if indice_fin > -1:
        return indice_debut, indice_fin
    else:
        return (0, 0)




def get_usefull_text(txt):
    if '#REDIRECT' in txt:
        print("Redirection link -> Remove killer from list\n")
    elif 'Infobox serial killer' in txt:
        print("Infobox Serial Killer")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox serial killer", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        print(txt[infobox_begin:infobox_end])
        print(txt[txt_begin:txt_end])
        print('\n')
    elif 'Infobox murderer' in txt:
        print("Infobox Murderer")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox murderer", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        print(txt[infobox_begin:infobox_end])
        print(txt[txt_begin:txt_end])
        print('\n')
    elif 'Infobox person' in txt:
        print("Infobox Person")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox person", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        print(txt[infobox_begin:infobox_end])
        print(txt[txt_begin:txt_end])
        print('\n')
    elif 'Infobox criminal' in txt:
        print("Infobox Criminal")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox criminal", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        print(txt[infobox_begin:infobox_end])
        print(txt[txt_begin:txt_end])
        print('\n')
    elif 'Infobox officeholder' in txt:
        print("Infobox Officeholder")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox officeholder", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        print(txt[infobox_begin:infobox_end])
        print(txt[txt_begin:txt_end])
        print('\n')
    elif 'Infobox' in txt:
        print("Other\n")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        print(txt[infobox_begin:infobox_end])
        print(txt[txt_begin:txt_end])
        print('\n')
    else:
        print("No infobox\n")


for killer in killer_list:
    get_usefull_text(killer[1])
