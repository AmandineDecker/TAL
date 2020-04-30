import nltk
import spacy


from Preprocessing import clean_text

nlp = spacy.load('en_core_web_sm')

infobox = '{{Infobox murderer\n| name        = Stoneman\n| image       = \n| image_size  =\n| caption     = \n| alt   ' \
          '      = \n| birth_name  = \n| alias       = <!--Alternate names or titles given to or taken by the killer, ' \
          'such as "The Boston Strangler", \n"Jack the Rip", "Son of Sam", etc.-->\n| birth_date  = <!-- {{birth ' \
          'date|YYYY|MM|DD}} if still living, use {{birth date and age|YYYY|MM|DD}} -->\n| birth_place = \n| ' \
          'death_date  = <!-- {{death date and age|YYYY|MM|DD|YYYY|MM|DD}} death date is first, birth date is ' \
          '\nsecond -->\n| death_place =\n| cause       = \n| conviction  = \n| sentence    = \n| victims     = ' \
          '13-26\n| beginyear   = 1985\n| endyear     = 1989\n| country     = [[India]]\n| states      = \n| ' \
          'apprehended = Unapprehended\n| imprisoned   =\n}} '
text = "The '''Stoneman''' is a name given by the popular English-language print media of [[Kolkata|Calcutta]], " \
       "[[India]] to an unidentified [[serial killer]] who murdered at least 13 homeless people of that city during " \
       "their sleep in 1989. The name is also given to the perpetrator of a similar series of murders in [[" \
       "Mumbai|Bombay]] from 1985 to 1988. It has been speculated that these were the work of the same person, " \
       "who could have been responsible for as many as 26 murders.\n\nThe Stoneman was blamed for thirteen murders " \
       "over six months (the first in June 1989), but it was never established whether the crimes were committed by " \
       "one person or a group of individuals. The [[Kolkata Police Force|Calcutta Police]] also failed to resolve " \
       "whether any of the crimes were committed as a [[copycat crimes|copycat murder]]. To date, no one has been " \
       "charged with any of the crimes; all thirteen cases remain unsolved.\n\n==Bombay killings==\nThe first hint of " \
       "a [[serial-killer]] who was targeting homeless ragpickers and beggars in India came from [[Bombay]]. Starting " \
       "in 1985, and lasting well over two years, a series of twelve murders were committed in the [[Sion, " \
       "India|Sion]] and [[King's Circle]] locality of the city. The criminal or criminals' ''modus operandi'' was " \
       "simple: first they would find an unsuspecting victim sleeping alone in a desolate area. The victim's head was " \
       "crushed with a single stone weighing as much as 30&nbsp;kg (~66 lbs). In most cases, the victims' identities " \
       "could not be ascertained since they slept alone and did not have relatives or associates who could identify " \
       "them. Compounded to this was the fact that the victims were people of very simple means and the individual " \
       "crimes were not high-profile. It was after the sixth murder that the [[Bombay Police]] began to see a pattern " \
       "in the crimes.\n\nA stroke of luck seemed to come the police's way when a homeless waiter survived a brutal " \
       "attack and managed to escape being bludgeoned to death. However, in the dimly lit area of Sion where he was " \
       "sleeping, he had not been able to get a good look at his assailant, and what seemed like a big break came to " \
       "naught.\n\nShortly afterwards, in 1987, a [[ragpicker]] was hacked to death in the adjoining suburb of [[" \
       "Matunga]]. Even though the police and the media were quick to label this the handiwork of the same person, " \
       "no evidence to link this crime with the others was ever found.\n\nAs mysteriously as the killings had " \
       "started, by the middle of 1988, they stopped. To this date the case is unsolved.\n\n==Summer of 1989 in " \
       "Calcutta==\nWhether or not the Bombay killings were linked to the Calcutta 'Stoneman' killings has never been " \
       "confirmed. However, the uncanny similarity in the instrument, choice of victims, execution, and the time of " \
       "the attacks suggests the assailant(s) was familiar with the Bombay episodes, if not the same killer " \
       "himself.\n\nThe first victim in Calcutta died from injuries to the head in June 1989. Twelve more would die " \
       "in the next six months as panic gripped the city. All of the murdered were homeless pavement-dwellers who " \
       "slept alone in dimly lit areas of the city. Most of the murders took place in central Calcutta, adjoining the " \
       "[[Howrah Bridge]].<ref name='ghoshhtimes'>{{cite web |last1=Ghosh |first1=Ritujay |title=The elusive stoneman " \
       "of Kolkata |url=https://www.hindustantimes.com/india/the-elusive-stoneman-of-kolkata/story" \
       "-BQBcCHfk87WvoLp2LSCKRN.html |website=HinduSan Stimes.com |publisher=Ritujay Ghosh |accessdate=11 October " \
       "2018}}</ref>\n\nBecause the murderer killed victims by dropping a heavy stone or concrete slab, the police " \
       "assumed that the assailant was probably a tall, well-built male. However, in the complete absence of any " \
       "eyewitnesses or survivors, no clear-cut leads were available.\n\nMassive deployments of police in various " \
       "parts of the city at night were resorted to, and numerous arrests were made. After a spell of arrests in " \
       "which a handful of 'suspicious persons' were rounded up for questioning, the killings stopped. However, " \
       "since there was no incriminating evidence, all those summarily arrested had to be released. To date, " \
       "the crimes remain unsolved.\n\n==Stoneman in Guwahati==\nSimilar incidents were reported in [[Guwahati]] city " \
       "of [[Assam]] state during February 2009.\n\n==Film adaptations based upon the events==\nProducer [[Bobby " \
       "Bedi]] produced a film titled ''[[The Stoneman Murders]]'' based on these incidents. The film released on 13 " \
       "February 2009, starring [[Kay Kay Menon]] and [[Arbaaz Khan]], and written and directed by [[Manish Gupta (" \
       "director)|Manish Gupta]]. Gupta said that his story for the movie is 40% fact and 60% fiction. The movie " \
       "depicts the killings to be a part of a religious ritual being conducted by a policeman, with the actual " \
       "perpetrator left open to interpretation at the end.\n\nIn 2011, a Bengali film named ''[[Baishe Srabon]]'' " \
       "released which was directed by Srijit Mukherjee. The plot of the movie revolved around the same mysterious " \
       "serial killings in Kolkata, which took place during the period of 1989. In the movie, the assassin is shown " \
       "to brutally murder and the victims mostly belonged to the ignoble and the plebeian league of the society; " \
       "either prostitutes, anti-socials or street dwellers. However, the climax of the movie saw the serial killer " \
       "shooting himself after confessing all his crudities, which, in fact, is a clear deviation from the actual " \
       "incident. "


def return_token(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte de chaque token
    return [X.text for X in doc]


from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))

clean_words = []
for token in return_token(text):
    if token not in stopWords:
        clean_words.append(token)


def return_NER(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner le texte et le label pour chaque entité
    return [(X.text, X.label_) for X in doc.ents]


def return_POS(sentence):
    # Tokeniser la phrase
    doc = nlp(sentence)
    # Retourner les étiquettes de chaque token
    return [(X, X.pos_) for X in doc]


def tokenize_in_sentences(txt):
    tokens = nltk.sent_tokenize(clean_text(txt))
    return tokens



def tokenize_and_tag(text, clean):
    # tokenize
    tokens = nltk.word_tokenize(text)
    if clean:  # clean tokens
        stopwords = set(nltk.corpus.stopwords.words("english"))
        tokens = [w for w in tokens if w not in stopwords]
    # tag
    tagged = nltk.pos_tag(tokens)
    # tagged.draw()
    # result
    return tagged


def get_ne(sentence):
    preprocessed = tokenize_and_tag(sentence, False)
    tree = nltk.ne_chunk(preprocessed, binary=True)  # binary -> NE
    neList = []
    for subtree in tree.subtrees():  # generate and go through subtrees
        # print("\nNew subtree")
        # print(subtree.label())
        if subtree.label() == "NE":
            for entity in subtree.subtrees():  # Get entities
                # print("\nNew entity")
                ne = ""
                for couple in entity:  # Rebuild entire entity
                    word = couple[0]  # Get world from the tuple
                    # print(word)
                    ne = ne + word + " "  # Add to final named entity
                # print(ne[:-1])
                neList.append(ne[:-1])  # add NE to the list
    print(neList)
    tree.draw()
    return neList