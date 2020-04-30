import collections
from lxml import etree
import re


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
        # print("Text not found")
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
        return (indice_debut, -1)


def get_usefull_text(txt):
    if '#REDIRECT' in txt:
        # print("Redirection link -> Remove killer from list\n")
        return "", ""
    elif 'Infobox serial killer' in txt:
        # print("Infobox Serial Killer")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox serial killer", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        # print(txt[infobox_begin:infobox_end])
        # print(txt[txt_begin:txt_end])
        # print('\n')
    elif 'Infobox murderer' in txt:
        # print("Infobox Murderer")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox murderer", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        # print(txt[infobox_begin:infobox_end])
        # print(txt[txt_begin:txt_end])
        # print('\n')
    elif 'Infobox person' in txt or 'Infobox Person' in txt:
        # print("Infobox Person")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox person", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        # print(txt[infobox_begin:infobox_end])
        # print(txt[txt_begin:txt_end])
        # print('\n')
    elif 'Infobox criminal' in txt:
        # print("Infobox Criminal")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox criminal", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        # print(txt[infobox_begin:infobox_end])
        # print(txt[txt_begin:txt_end])
        # print('\n')
    elif 'Infobox officeholder' in txt:
        # print("Infobox Officeholder")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox officeholder", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        # print(txt[infobox_begin:infobox_end])
        # print(txt[txt_begin:txt_end])
        # print('\n')
    elif 'Infobox' in txt:
        # print("Other\n")
        (infobox_begin, infobox_end) = get_text_between_brackets("Infobox", txt)
        (txt_begin, txt_end) = get_text_before_see_also(txt, infobox_end + 1)
        # print(txt[infobox_begin:infobox_end])
        # print(txt[txt_begin:txt_end])
        # print('\n')
    else:
        (infobox_begin, infobox_end) = (0, 0)
        (txt_begin, txt_end) = get_text_before_see_also(txt, 0)
        # print("No infobox\n")
        # print(txt[txt_begin:txt_end])
        # print('\n')
    return txt[infobox_begin:infobox_end], txt[txt_begin:txt_end]


def remove_refs(txt):  # Retire ref /ref et ce qu'il y a entre
    return re.sub(r'ref.*?/ref', '', txt, flags=re.DOTALL)


def remove_ref_name(txt):  # Retire <ref name = ...>  (< = &lt; et > = &gt;)
    txt = re.sub('&lt;ref name=.*?&gt;', '', txt, flags=re.MULTILINE)
    return re.sub(r'<ref name=.*?>', '', txt, flags=re.MULTILINE)


def remove_reflist(txt):
    return re.sub(r'{{Reflist}}.*', '', txt, flags=re.MULTILINE)


def remove_quotes(txt):
    txt = re.sub(r'{{quote.*?}}', '', txt, flags=re.DOTALL)
    return re.sub(r'{{Quote.*?}}', '', txt, flags=re.DOTALL)


def remove_see_also(txt):
    return re.sub(r'{{See also.*?}}', '', txt, flags=re.DOTALL)


def remove_files(txt):
    return re.sub(r'File:.*?.jpg.*?\n', '', txt, flags=re.DOTALL)


def remove_star_list(txt):
    return re.sub(r'<\*.*?\n>*', '', txt, flags=re.DOTALL)


def remove_repeats(txt):  # Remplace [[A|B]] par A
    return re.sub(r'\[\[(?P<name>.*?)\|.*?\]\]', r'\1', txt, flags=re.DOTALL)


def remove_brackets(txt):
    return re.sub(r'{{(?P<name>.*?)}}', r'\1', txt, flags=re.DOTALL)


def remove_specials(txt):
    txt = re.sub("\[|\]|<>|<|>|\'+|&nbsp;|&lt;|&gt;", '', txt, flags=re.MULTILINE)
    return txt


def remove_titels(txt):
    txt = re.sub(r'==*.*?==*', '', txt, flags=re.DOTALL)
    return txt


def clean_text(txt):
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
    # text = remove_titels(text)
    return text


# print(clean_text('One time, to escape police arrest, Jesus Silva hid himself in the housing of a public telephone.&lt;ref name="chucky"/&gt; And sometimes was carried by a tall friend on the shoulder to fire with a sub-machine gun.&lt;ref name="chucky"/&gt;&lt;ref name="jesus silva"/&gt; On one occasion, during a police investigation in a morro in Salvador, several teams were attempting to capture a bandit. By radio, police officers communicated about the operation and the warning that the bandit walked off the morro. Jesus Silva had dribbled the police: When the police officers were discussing if the criminal had escaped, one of the officers said: "Only a dwarf has walked", one police officers responded: "The dwarf was the man!", but Jesus Silva had already escaped.&lt;ref name="chucky"/&gt;&lt;ref name="jesus silva"/&gt;'))

for killer in killer_list:
    infobox, text = get_usefull_text(killer[1])
    # print("Infobox:\n\n" + infobox + "\n\n\n")
    # print(clean_text(text))
    # print('\n\n\n')
