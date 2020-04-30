import nltk
import re

from Preprocessing import make_killer_list, get_usefull_text, clean_text
from Tokenize import tokenize_in_sentences
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


def get_text(clean):
    killer_list = make_killer_list()
    all_text = []
    for killer in killer_list:
        infobox, text = get_usefull_text(killer[1])
        if clean:
            all_text.append((killer[0], clean_text(text)))
        else:
            all_text.append((killer, text))
    return all_text


def print_text(text):
    print("***   " + text[0] + "   ***")
    print()
    print(text[1])


def get_parts_titels(text):
    parts_titels = re.findall(r'==*(?P<name>.*?)==*', text)
    return parts_titels


def analyse_parts_titels(text):
    parts_titels = get_parts_titels(text)
    lemmatizer = WordNetLemmatizer()
    syn_murder = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="v")) + wn.synsets(
        lemmatizer.lemmatize('murder', pos="n")) + wn.synsets(lemmatizer.lemmatize('homicide', pos="n")) + wn.synsets(
        lemmatizer.lemmatize('killings', pos="n")) + wn.synsets(lemmatizer.lemmatize('assassination', pos="n"))]
    for titel in parts_titels:
        for t in nltk.word_tokenize(titel):
            if lemmatizer.lemmatize(t, pos="v") in syn_murder or lemmatizer.lemmatize(t, pos="n") in syn_murder:
                print(titel)


def is_usefull_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    syn_murder = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder'))]
    tokens = nltk.word_tokenize(sentence)
    for t in tokens:
        if lemmatizer.lemmatize(t, pos="v") in syn_murder or lemmatizer.lemmatize(t, pos="n") in syn_murder:
            # print(t)
            return True
    return False


def is_sentence_with_verb_kill(sentence):
    lemmatizer = WordNetLemmatizer()
    syn_murder = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="v"))]
    tokens = nltk.word_tokenize(sentence)
    for t in tokens:
        if lemmatizer.lemmatize(t, pos="v") in syn_murder:
            # print(t)
            return True
    return False


def is_sentence_with_noun_kill(sentence):
    lemmatizer = WordNetLemmatizer()
    syn_murder = [w.lemma_names()[0] for w in
                  wn.synsets(lemmatizer.lemmatize('murder')) + wn.synsets(lemmatizer.lemmatize('poison'))]
    tokens = nltk.word_tokenize(sentence)
    for t in tokens:
        if lemmatizer.lemmatize(t, pos="n") in syn_murder:
            # print(t)
            return True
    return False


def get_usefull_sentences_verb(text):
    sentences = tokenize_in_sentences(text[1])
    usefull_sentences = []
    for sentence in sentences:
        if is_sentence_with_verb_kill(sentence):
            # print(sentence)
            usefull_sentences.append(sentence)
    return usefull_sentences


def get_usefull_sentences_noun(text):
    sentences = tokenize_in_sentences(text[1])
    usefull_sentences = []
    for sentence in sentences:
        if is_sentence_with_noun_kill(sentence):
            usefull_sentences.append(sentence)
    return usefull_sentences


# Les victimes

def process_content(text):
    sentences = set(get_usefull_sentences_verb(text) + get_usefull_sentences_noun(text))
    chunks = []
    try:
        for sentence in sentences:
            sentence = re.sub(',', '', sentence)
            words = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(words)
            ne = nltk.ne_chunk(tagged, binary=False)

            chunk_gram = r"""Chunk: {<IN>*?<NNP>*?<VB.?|NN|NNP|DT>+<IN>*?<...?.?>*?<NNP|CD>+<NN>*?}"""

            chunk_parser = nltk.RegexpParser(chunk_gram)
            chunked = chunk_parser.parse(tagged)

            # chunked.draw()
            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                chunks.append(subtree)
                # print(subtree)
    except Exception as e:
        print(e)
    return chunks


def get_ne(text):
    sentences = get_usefull_sentences_verb(text)
    chunks = []
    for sentence in sentences:
        words = nltk.pos_tag(nltk.word_tokenize(sentence))
        tagged = nltk.ne_chunk(words, binary=False)

        for ne in tagged:
            print(ne)


def analyse_chunk(chunk):
    persons = []
    chunk_gram = r"""Verb: {<VB.?>}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(chunk)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Verb'):
        chunks.append(subtree)
    if chunks != []:
        verb = chunks[0][0][0]
        lemmatizer = WordNetLemmatizer()
        syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="v"))])
        # print(verb)
        # print(lemmatizer.lemmatize(verb, pos="v") in syn_murder)
        if lemmatizer.lemmatize(verb, pos="v") in syn_murder:
            tagged = nltk.ne_chunk(chunk, binary=False)
            for ne in tagged.subtrees():
                if ne.label() == 'PERSON':
                    person = ""
                    for node in ne:
                        # print(node[0])
                        person = person + " " + node[0]
                    persons.append(person[1:])
    # if len(persons) > 0:
    # print(persons)
    return persons


def analyse_chunk_bis(chunk):
    persons = []
    chunk_gram = r"""Murder: {<NN|NNS><IN>}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(chunk)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        chunks.append(subtree)
    if chunks != []:
        # print(chunks)
        noun = chunks[0][0][0]
        # print(noun)
        lemmatizer = WordNetLemmatizer()
        syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
        # print(verb)
        # print(lemmatizer.lemmatize(verb, pos="v") in syn_murder)
        if lemmatizer.lemmatize(noun, pos="n") in syn_murder:
            tagged = nltk.ne_chunk(chunk, binary=False)
            for ne in tagged.subtrees():
                if ne.label() == 'PERSON':
                    person = ""
                    for node in ne:
                        # print(node[0])
                        person = person + " " + node[0]
                    persons.append(person[1:])
    # if len(persons) > 0:
    # print(persons)
    return persons


def analyse_chunk_ter(chunk):
    persons = []
    places = []
    chunk_gram = r"""Murder: {<NN|NNS><IN>}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(chunk)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        chunks.append(subtree)
    if chunks != []:
        # print(chunks)
        noun = chunks[0][0][0]
        prep = chunks[0][1][0]
        # print(prep)
        # print(noun)
        lemmatizer = WordNetLemmatizer()
        syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
        # print(verb)
        # print(lemmatizer.lemmatize(verb, pos="v") in syn_murder)
        if lemmatizer.lemmatize(noun, pos="n") in syn_murder:
            tagged = nltk.ne_chunk(chunk, binary=False)
            for ne in tagged.subtrees():
                if ne.label() in ['GPE', 'LOC']:
                    if prep == 'of':
                        person = ""
                        for node in ne:
                            # print(node[0])
                            person = person + " " + node[0]
                        persons.append(person[1:])
                    else:
                        place = ""
                        for node in ne:
                            # print(node[0])
                            place = place + " " + node[0]
                        places.append(place[1:])
    # if len(persons) > 0:
    # print('Persons')
    # print(chunk)
    # print(persons)
    # if len(places) > 0:
    # print('Places')
    # print(chunk)
    # print(places)
    return persons, places


def analyse_chunk_quater(chunk):
    dates = []
    chunk_gram = r"""Murder: {<NN|NNS><IN><NNP>?<CD>+<CC>?<IN>?<NNP>?<CD>?}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(chunk)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        chunks.append(subtree)
    if chunks != []:
        # print(chunks)
        noun = chunks[0][0][0]
        # print(noun)
        lemmatizer = WordNetLemmatizer()
        syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
        # print(verb)
        # print(lemmatizer.lemmatize(verb, pos="v") in syn_murder)
        if lemmatizer.lemmatize(noun, pos="n") in syn_murder:
            chunk_gram_date = r"""Date: {<IN>?<NNP>?<CD>+<CC>?<IN>?<NNP>?<CD>?}"""
            chunk_parser_date = nltk.RegexpParser(chunk_gram_date)
            chunked_date = chunk_parser_date.parse(chunk)
            chunks_date = []
            for subtree in chunked_date.subtrees(filter=lambda t: t.label() == 'Date'):
                chunks_date.append(subtree)
                if chunks_date != []:
                    date = ""
                    for x in subtree:
                        if x[1] in ['NNP', 'CD']:
                            date = date + " " + x[0]
                    if re.search("""(1|2|3|4|5|6|7|8|9|0){4}""", date[1:]) != None:
                        dates.append(date[1:])
                    # print(chunks_date[0])
    # if len(dates) > 0:
        # print(dates)
    return dates


def clean_set(set):
    a_supprimer = []
    for element in set:
        for s in set:
            if element in s and element != s:
                a_supprimer.append(element)
    for x in a_supprimer:
        set.remove(x)
    return set


def get_victims(text):
    lemmatizer = WordNetLemmatizer()
    chunks = process_content(text)
    victims = []
    for chunk in chunks:
        # print(chunk)
        victims = victims + analyse_chunk(chunk) + analyse_chunk_bis(chunk) + analyse_chunk_ter(chunk)[0]
    killer = text[0]
    victims = set(victims)
    to_remove = []
    for x in victims:
        if killer in x or x in killer:
            to_remove.append(x)
    for x in to_remove:
        victims.remove(x)
    return clean_set(victims)


def get_places(text):
    lemmatizer = WordNetLemmatizer()
    chunks = process_content(text)
    places = []
    for chunk in chunks:
        # print(chunk)
        places = places + analyse_chunk_ter(chunk)[1]
    killer = text[0]
    places = set(places)
    # to_remove = []
    # for x in places:
    #     if killer in x or x in killer:
    #         to_remove.append(x)
    # for x in to_remove:
    #     places.remove(x)
    return clean_set(places)


def get_dates(text):
    lemmatizer = WordNetLemmatizer()
    chunks = process_content(text)
    dates = []
    for chunk in chunks:
        # print(chunk)
        dates = dates + analyse_chunk_quater(chunk)
    dates = set(dates)
    return clean_set(dates)



def precise_process_content(text):
    sentences = set(get_usefull_sentences_verb(text) + get_usefull_sentences_noun(text))
    chunks = []
    try:
        for sentence in sentences:
            sentence = re.sub(',', '', sentence)
            words = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(words)
            # ne = nltk.ne_chunk(tagged, binary=False)

            chunk_gram = r"""Chunk: {<IN><NNP>*?<CD>+<NN|NNP|DT|PRP.?>+<VB.?><...?.?>*?<NN.?.?><IN>*?<...?.?>*?<NNP|CD>+<NN>*?}"""

            chunk_parser = nltk.RegexpParser(chunk_gram)
            chunked = chunk_parser.parse(tagged)

            # chunked.draw()
            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                chunks.append(subtree)
                # print(subtree)
    except Exception as e:
        print(e)
    return chunks

def analyse_precise_chunk(chunk):
    dates = []
    victims = []

    chunk_gram_date = r"""Date: {<IN>?<NNP>?<CD>+}"""
    chunk_gram_victim_verb = r"""Murder: {<VBD><PRP.?>?<JJ>?<NN>?<JJ>*<NNP>+}"""
    chunk_gram_victim_noun = r"""Murder: {<NN><IN><PRP.?>?<JJ>?<NN.?>+}"""

    chunk_parser = nltk.RegexpParser(chunk_gram_date)
    chunked = chunk_parser.parse(chunk)
    chunks_dates = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Date'):
        chunks_dates.append(subtree)
        if chunks_dates != []:
            # print(chunks_dates)
            date = ""
            for x in subtree:
                if x[1] in ['NNP', 'CD']:
                    date = date + " " + x[0]
            if re.search("""(1|2|3|4|5|6|7|8|9|0){4}""", date[1:]) != None:
                dates.append(date[1:])
            # print(dates)

    chunk_parser = nltk.RegexpParser(chunk_gram_victim_verb)
    chunked = chunk_parser.parse(chunk)
    chunks_victims = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        # print(subtree)
        chunks_victims.append(subtree)
        if chunks_victims != []:
            verb = chunks_victims[0][0][0]
            # print(verb)
            lemmatizer = WordNetLemmatizer()
            syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="v")) + wn.synsets(lemmatizer.lemmatize('attack', pos="v"))])
            # print(verb)
            # print(lemmatizer.lemmatize(verb, pos="v") in syn_murder)
            if lemmatizer.lemmatize(verb, pos="v") in syn_murder:
                victim = ""
                for node in subtree[1:]:
                        # print(node[0])
                        victim = victim + " " + node[0]
                victims.append(victim[1:])
                # print(victims)
    if victims == []: # On travaille avec Murder(s) of...
        chunk_parser = nltk.RegexpParser(chunk_gram_victim_noun)
        chunked = chunk_parser.parse(chunk)
        chunks_victims = []
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
            chunks_victims.append(subtree)
            if chunks_victims != []:
                # print(chunks_victims)
                noun = chunks_victims[0][0][0]
                # print(noun)
                prep = chunks_victims[0][1][0]
                # print(prep)
                lemmatizer = WordNetLemmatizer()
                syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
                if lemmatizer.lemmatize(noun, pos="n") in syn_murder and prep == 'of':
                    victim = ""
                    for node in subtree[2:]:
                        # print(node[0])
                        victim = victim + " " + node[0]
                    victims.append(victim[1:])
                    # print(victims)
    if victims != [] and dates != []:
        return (victims[0], dates[0])

def get_precise_infos(text):
    chunks = precise_process_content(text)
    infos = []
    for chunk in chunks:
        # print(chunk)
        infos.append(analyse_precise_chunk(chunk))
    return infos

#
# all_text = get_text(True)
# #
# chunks = []
# for text in all_text:
#     print(text[0])
#     print()
#     # print('Victims')
#     # print(get_victims(text))
#     # print('Places')
#     # print(get_places(text))
#     # print('Dates')
#     # print(get_dates(text))
#
#     chunks = precise_process_content(text)
#     for chunk in chunks:
#         # print(chunk)
#         print(analyse_precise_chunk(chunk))
#     #     analyse_chunk_quater(chunk)
#     #     # analyse_chunk_ter(chunk)
#
#     print('****************************************')
    # chunks = process_content(text)

# tree = chunks[4]
# print(tree)
# print(tree[0][0])
# print(tree[1])
# s = 'He committed murders between 2000 and 2006 in Shchuchyn District and Grodno District.'
# sentence = re.sub(',', '', s)
# words = nltk.word_tokenize(sentence)
# tagged = nltk.pos_tag(words)
# print(tagged)
