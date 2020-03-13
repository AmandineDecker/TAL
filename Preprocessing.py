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


#  display tags of the tree, with or without namespace
def display(tree, with_namespace):
    if not with_namespace:  # removes namespaces
        tree = strip_ns_prefix(tree)

    nice_tree = collections.OrderedDict()

    for tag in tree.iter():  # get tags
        path = re.sub('\[[0-9]+\]', '', tree.getpath(tag))
        if path not in nice_tree:
            nice_tree[path] = []
        if len(tag.keys()) > 0:
            nice_tree[path].extend(attrib for attrib in tag.keys() if attrib not in nice_tree[path])

    for path, attribs in nice_tree.items():  # print with indent
        indent = int(path.count('/') - 1)
        print('{0}{1}: {2} [{3}]'.format('    ' * indent, indent, path.split('/')[-1],
                                         ', '.join(attribs) if len(attribs) > 0 else '-'))


wiki_tree = etree.parse('Wikipedia_Corpus.xml')
print('\n\n REMOVING NAMESPACES \n\n')
display(wiki_tree, False)

print("\n\n**************************************************\n")
killers_list = []
for user_id in range(len(wiki_tree.xpath("/mediawiki/page"))):
    name = wiki_tree.xpath("/mediawiki/page/title")[user_id].text
    txt = wiki_tree.xpath("/mediawiki/page/revision/text")[user_id].text
    killer = (name, txt)
    killers_list.append(killer)
    # print(killer)
print(killers_list)