import nltk
import TokensChunk
from Other import clean_set

from Preprocessing import make_killer_list, get_usefull_text, clean_text
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


# Renvoie une liste contenant le texte utile de chaque page Wikipedia du corpus
def get_all_text(clean):
    killer_list = make_killer_list()
    all_text = []
    for killer in killer_list:
        infobox, text = get_usefull_text(killer[1])
        if clean:
            all_text.append((killer[0], clean_text(text)))
        else:
            all_text.append((killer, text))
    return all_text


# Renvoie le l'infobox et le texte d'un tueur
def get_text(number, clean):
    killer_list = make_killer_list()
    killer = killer_list[number]
    infobox, text = get_usefull_text(killer[1])
    if clean:
        text = (killer[0], clean_text(text))
    else:
        text = (killer, text)
    return (killer, infobox), text

# Renvoie True si la phrase contient un synonyme du verbe "tuer"
def is_sentence_with_verb_kill(sentence):
    lemmatizer = WordNetLemmatizer()
    syn_murder = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder', pos="v"))]
    tokens = nltk.word_tokenize(sentence)
    for t in tokens:
        if lemmatizer.lemmatize(t, pos="v") in syn_murder:
            return True
    return False


# Renvoie les phrases qui contiennent un synonyme du verbe "tuer"
def get_usefull_sentences_verb(text):
    sentences = TokensChunk.tokenize_in_sentences(text[1])
    usefull_sentences = []
    for sentence in sentences:
        if is_sentence_with_verb_kill(sentence):
            usefull_sentences.append(sentence)
    return usefull_sentences


# Renvoie True si la phrase contient un synonyme du nom "meurtre"
def is_sentence_with_noun_kill(sentence):
    lemmatizer = WordNetLemmatizer()
    syn_murder = [w.lemma_names()[0] for w in wn.synsets(lemmatizer.lemmatize('murder'))]
    tokens = nltk.word_tokenize(sentence)
    for t in tokens:
        if lemmatizer.lemmatize(t, pos="n") in syn_murder:
            return True
    return False


# Renvoie les phrases qui contiennent un synonyme du nom "meurtre"
def get_usefull_sentences_noun(text):
    sentences = TokensChunk.tokenize_in_sentences(text[1])
    usefull_sentences = []
    for sentence in sentences:
        if is_sentence_with_noun_kill(sentence):
            usefull_sentences.append(sentence)
    return usefull_sentences


# Renvoie un set contenant les victimes trouvées dans la partie liée au meurtre dans text
def get_victims(text):
    chunks = TokensChunk.process_content(text)
    victims = []
    for chunk in chunks:
        victims = victims + TokensChunk.analyse_chunk_person_verb(chunk) + TokensChunk.analyse_chunk_person_noun(chunk) + \
                  TokensChunk.analyse_chunk_person_place(chunk)[0]
    killer = text[0]
    victims = set(victims)
    to_remove = []
    for x in victims:
        if killer in x or x in killer:
            to_remove.append(x)
    for x in to_remove:
        victims.remove(x)
    return clean_set(victims)


# Renvoie un set contenant les lieux trouvés dans la partie liée au meurtre dans text
def get_places(text):
    chunks = TokensChunk.process_content(text)
    places = []
    for chunk in chunks:
        places = places + TokensChunk.analyse_chunk_person_place(chunk)[1]
    places = set(places)
    return clean_set(places)


# Renvoie un set contenant les dates trouvées dans la partie liée au meurtre de text
def get_dates(text):
    chunks = TokensChunk.process_content(text)
    dates = []
    for chunk in chunks:
        dates = dates + TokensChunk.analyse_chunk_dates(chunk)
    dates = set(dates)
    return clean_set(dates)


# Renvoie une liste de tuples (victime, date) trouvés dans la partie liée au meurtre dans text
def get_precise_infos(text):
    chunks = TokensChunk.precise_process_content(text)
    infos = []
    for chunk in chunks:
        info = TokensChunk.analyse_precise_chunk(chunk)
        if info != None:
            infos.append(TokensChunk.analyse_precise_chunk(chunk))
    return infos
