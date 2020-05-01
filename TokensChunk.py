import nltk
import Text
import re

from Preprocessing import clean_text
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


def tokenize_in_sentences(txt):
    tokens = nltk.sent_tokenize(clean_text(txt))
    return tokens


# Renvoie les chunk contenant le motif <IN>*?<NNP>*?<VB.?|NN|NNP|DT>+<IN>*?<...?.?>*?<NNP|CD>+<NN>*?
def process_content(text):
    sentences = set(Text.get_usefull_sentences_verb(text) + Text.get_usefull_sentences_noun(text))
    chunks = []
    try:
        for sentence in sentences:
            sentence = re.sub(',', '', sentence)
            words = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(words)
            ne = nltk.ne_chunk(tagged, binary=False)

            chunk_gram = r"""Chunk: {<VB.?|NN|NNP|DT>+<IN>*?<...?.?>*?<NNP|CD>+<NN>*?}"""

            chunk_parser = nltk.RegexpParser(chunk_gram)
            chunked = chunk_parser.parse(tagged)

            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                chunks.append(subtree)
    except Exception as e:
        print(e)
    return chunks


# Analyse un chunk, s'il contient un synonyme du verbe tuer suivi d'une entité nommée de type Person alors il la renvoie
def analyse_chunk_person_verb(chunk):
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
        if lemmatizer.lemmatize(verb, pos="v") in syn_murder:
            tagged = nltk.ne_chunk(chunk, binary=False)
            for ne in tagged.subtrees():
                if ne.label() == 'PERSON':
                    person = ""
                    for node in ne:
                        person = person + " " + node[0]
                    persons.append(person[1:])
    return persons


# Analyse un chunk, s'il contient un synonyme du nom meurtre suivi d'une entité nommée de type Person alors il la renvoie
def analyse_chunk_person_noun(chunk):
    persons = []
    chunk_gram = r"""Murder: {<NN|NNS><IN>}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(chunk)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        chunks.append(subtree)
    if chunks != []:
        noun = chunks[0][0][0]
        lemmatizer = WordNetLemmatizer()
        syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
        if lemmatizer.lemmatize(noun, pos="n") in syn_murder:
            tagged = nltk.ne_chunk(chunk, binary=False)
            for ne in tagged.subtrees():
                if ne.label() == 'PERSON':
                    person = ""
                    for node in ne:
                        person = person + " " + node[0]
                    persons.append(person[1:])
    return persons


# Analyse un chunk, s'il contient un synonyme du nom meurtre suivi d'une préposition puis d'une entité nommée de type
# LOC ou GPE alors il la renvoie, en tant que lieux si la préposition est 'in', en tant que personne sinon
def analyse_chunk_person_place(chunk):
    persons = []
    places = []
    chunk_gram = r"""Murder: {<NN|NNS><IN>}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(chunk)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        chunks.append(subtree)
    if chunks != []:
        noun = chunks[0][0][0]
        prep = chunks[0][1][0]
        lemmatizer = WordNetLemmatizer()
        syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
        if lemmatizer.lemmatize(noun, pos="n") in syn_murder:
            tagged = nltk.ne_chunk(chunk, binary=False)
            for ne in tagged.subtrees():
                if ne.label() in ['GPE', 'LOC']:
                    if prep == 'of':
                        person = ""
                        for node in ne:
                            person = person + " " + node[0]
                        persons.append(person[1:])
                    else:
                        place = ""
                        for node in ne:
                            place = place + " " + node[0]
                        places.append(place[1:])
    return persons, places


# Analyse un chunk pour y trouver des dates: cherche les cardinaux (CD) et éventuellement les noms propres (NNP),
# si le chunk contient au moins un nombre à 4 chiffres alors il est renvoyé
def analyse_chunk_dates(chunk):
    dates = []
    chunk_gram = r"""Murder: {<NN|NNS><IN><NNP>?<CD>+<CC>?<IN>?<NNP>?<CD>?}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(chunk)
    chunks = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        chunks.append(subtree)
    if chunks != []:
        noun = chunks[0][0][0]
        lemmatizer = WordNetLemmatizer()
        syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
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
    return dates


# Renvoie les chunk contenant le motif <IN><NNP>*?<CD>+<NN|NNP|DT|PRP.?>+<VB.?><...?.?>*?<NN.?.?><IN>*?<...?.?>*?<NNP|CD>+<NN>*?
def precise_process_content(text):
    sentences = set(Text.get_usefull_sentences_verb(text) + Text.get_usefull_sentences_noun(text))
    chunks = []
    try:
        for sentence in sentences:
            sentence = re.sub(',', '', sentence)
            words = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(words)

            chunk_gram = r"""Chunk: {<IN><NNP>*?<CD>+<NN|NNP|DT|PRP.?>+<VB.?><...?.?>*?<NN.?.?><IN>*?<...?.?>*?<NNP|CD>+<NN>*?}"""

            chunk_parser = nltk.RegexpParser(chunk_gram)
            chunked = chunk_parser.parse(tagged)

            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                chunks.append(subtree)

    except Exception as e:
        print(e)
    return chunks


# Analyse le chunk pour y chercher une date et une victime
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
            date = ""
            for x in subtree:
                if x[1] in ['NNP', 'CD']:
                    date = date + " " + x[0]
            if re.search("""(1|2|3|4|5|6|7|8|9|0){4}""", date[1:]) != None:
                dates.append(date[1:])

    chunk_parser = nltk.RegexpParser(chunk_gram_victim_verb)
    chunked = chunk_parser.parse(chunk)
    chunks_victims = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
        chunks_victims.append(subtree)
        if chunks_victims != []:
            verb = chunks_victims[0][0][0]
            lemmatizer = WordNetLemmatizer()
            syn_murder = set([w.lemma_names()[0] for w in
                              wn.synsets(lemmatizer.lemmatize('murder', pos="v")) + wn.synsets(
                                  lemmatizer.lemmatize('attack', pos="v"))])
            if lemmatizer.lemmatize(verb, pos="v") in syn_murder:
                victim = ""
                for node in subtree[1:]:
                    victim = victim + " " + node[0]
                victims.append(victim[1:])
    if victims == []:  # On travaille avec Murder(s) of...
        chunk_parser = nltk.RegexpParser(chunk_gram_victim_noun)
        chunked = chunk_parser.parse(chunk)
        chunks_victims = []
        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Murder'):
            chunks_victims.append(subtree)
            if chunks_victims != []:
                noun = chunks_victims[0][0][0]
                prep = chunks_victims[0][1][0]
                lemmatizer = WordNetLemmatizer()
                syn_murder = set([w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="n"))])
                if lemmatizer.lemmatize(noun, pos="n") in syn_murder and prep == 'of':
                    victim = ""
                    for node in subtree[2:]:
                        victim = victim + " " + node[0]
                    victims.append(victim[1:])
    if victims != [] and victims != None and dates != [] and dates != None:
        return (victims[0], dates[0])
