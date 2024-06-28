#!venv/bin/python3
"""
Generate word clouds from documents in my portfolio
"""

import collections
import logging
import re

import matplotlib.pyplot as plt
import nltk
import wordcloud

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from collections import defaultdict
from spacy.lang.en import stop_words

nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('words')

logger = logging.getLogger(__name__)


def case_insensitive_replace(string_to_replace, replacement_string,
                             original_string):
    """
    Replace all instances of old_string with a new_string in text
    regardless of case.

    :param string_to_replace: The original string.
    :type string_to_replace: str
    :param replacement_string: The new string.
    :type replacement_string: str
    :param original_string: The text in which to perform the
    replacement.
    :type original_string: str
    :return: The text after performing the replacement.
    :rtype: str

    See `https://stackoverflow.com/questions/919056/case-insensitive-replace`
    """
    return re.sub('(?i)' + re.escape(string_to_replace),
                  lambda m: replacement_string, original_string)


# See https://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-list
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def case_insensitive_remove_values_from_list(the_list,
                                             value_to_remove):
    return [value for value in the_list if
            value.lower() != value_to_remove.lower()]


def write_string_to_file(the_string, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(the_string)


def make_one_word_cloud(text_path: str, image_path: str):
    """
    Make a single word cloud image from a single text file.

    :param text_path: Path to the text file that serves as input.
    :param image_path: Path to the image file that will result.
    :return:
    """
    # Extract text from PDF
    # pdfFileObj = open('_portfolio/scaling_up_romania.pdf', 'rb')
    # pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
    # text = ''
    # for page in pdfReader.pages:
    #     text += page.extractText()
    # pdfFileObj.close()
    # text = text.replace("\n-", "")

    # Avoid text from PDFs, which is full of OCR garbage in many cases
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.replace("\n", " ")
    # text = text.translate(str.maketrans('', '', string.punctuation))  # Remove all punctuation
    # Remove short words
    text = " ".join(word for word in text.split() if len(word) > 2)
    # Remove possessives with curly quotes, which show up as their own words with space in them
    text = case_insensitive_replace("’s", "", text)

    # Keep a copy for debugging
    write_string_to_file(text, "original.txt")

    # Stem (lemmatize) and drop non-English words

    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    # tokens = word_tokenize(text)
    delimiters = {r"\s+", ";", ":", ".", "(", ")", "/", "“", "”"}
    regexp = r"[" + "|".join(delimiters) + r"]\s*"
    logger.debug("Regexp:", "<" + regexp + ">")
    tokens = re.split(regexp, text)
    logger.debug("Tokens: " + " ".join(tokens))

    tokens = [token for token in tokens if token not in delimiters]
    logger.debug("Tokens: " + " ".join(tokens))
    words = set(nltk.corpus.words.words())
    custom_words = {"blockchain", "broadband", "challenges",
                    "database", "developing", "economies",
                    "ecosystems", "entrepreneurs", "firms",
                    "guatemala", "high-tech", "honduras",
                    "indicators", "jobs", "logframe", "manufacturing",
                    "msme", "msmes", "opportunities", "r&d", "sme",
                    "smes", "nicaragua", "robotics", "salvador",
                    "start-up", "startup", "technologies",
                    "washington", "women"}
    lemma_function = WordNetLemmatizer()
    text_list = []
    for token, tag in pos_tag(tokens):
        lemma = lemma_function.lemmatize(token, tag_map[tag[0]])
        lemma = lemma.lower()
        if len(lemma) > 2 and lemma not in stop_words.STOP_WORDS and (lemma in words or lemma in custom_words):
            text_list.append(lemma)
            logger.debug(
                "Accepted: '" + token + "' => '" + lemma + "'")
        else:
            logger.debug(
                "Rejected: '" + token + "' => '" + lemma + "'")

    text = " ".join(text_list)

    # snow_stemmer = SnowballStemmer(language='english')
    # words = set(nltk.corpus.words.words())
    # text = " ".join(snow_stemmer.stem(w) for w in nltk.wordpunct_tokenize(text) if snow_stemmer.stem(w) in words)
    write_string_to_file(text, "english.txt")

    # Remove consecutive duplicates
    # See https://stackoverflow.com/questions/39237350/how-do-i-remove-consecutive-duplicates-from-a-list
    # english_words = [k for k, g in itertools.groupby(english_words)]

    # Remove some useless words
    # english_words = case_insensitive_remove_values_from_list(english_words, "and")
    # english_words = case_insensitive_remove_values_from_list(english_words, "apter")
    # english_words = case_insensitive_remove_values_from_list(english_words, "bucharest")
    # english_words = case_insensitive_remove_values_from_list(english_words, "figure")
    # english_words = case_insensitive_remove_values_from_list(english_words, "manufacture")

    # english_words = case_insensitive_remove_values_from_list(english_words, "per")
    # english_words = case_insensitive_remove_values_from_list(english_words, "practices")
    # english_words = case_insensitive_remove_values_from_list(english_words, "romania")
    # english_words = case_insensitive_remove_values_from_list(english_words, "ross")
    # english_words = case_insensitive_remove_values_from_list(english_words, "source")
    # english_words = case_insensitive_remove_values_from_list(english_words, "world bank")
    # english_words = case_insensitive_remove_values_from_list(english_words, "world bank group")

    # Do some lemmatization by hand
    # english_text = " ".join(english_words)
    # english_text = text
    # english_text = case_insensitive_replace("entrepreneurial", "entrepreneurship", english_text)
    # english_text = case_insensitive_replace("instruments", "instrument", english_text)
    # english_text = case_insensitive_replace("romanian", "romania", english_text)
    # english_text = case_insensitive_replace("romania's", "romania", english_text)
    # english_text = case_insensitive_replace("scores", "score", english_text)
    # english_text = case_insensitive_replace("startups", "startup", english_text)

    # Try to correct spelling
    # blob = textblob.blob.TextBlob(text)

    # blob.correct() - too slow

    # Do automated lemmatization
    # singular_list = [word.lemmatize() for word in blob.words]
    # singular_list = remove_values_from_list(singular_list, "wa")  # Somehow introduced by TextBlob
    # singular_text = " ".join(singular_list)
    # write_string_to_file(singular_text, "singular.txt")
    # singular_blob = textblob.blob.TextBlob(singular_text)

    frequencies = collections.Counter()
    for word in text.split(" "):
        frequencies[word] += 1

    frequencies = dict(frequencies)

    logger.debug("smes: " + str(frequencies["smes"]))
    logger.debug("msmes: " + str(frequencies["msmes"]))

    # # Get frequencies of noun phrases
    # frequencies = blob.np_counts
    #
    # # Remove short words (again)
    # frequencies = {key: frequencies[key] for key in frequencies if len(key) > 2}

    # Remove distractors
    frequencies.pop("and", None)
    frequencies.pop("can", None)
    frequencies.pop("figure", None)
    frequencies.pop("for", None)
    frequencies.pop("from", None)
    frequencies.pop("have", None)
    frequencies.pop("number", None)
    frequencies.pop("romania", None)
    frequencies.pop("romanian", None)
    frequencies.pop("source", None)
    frequencies.pop("than", None)
    frequencies.pop("that", None)
    frequencies.pop("the", None)
    frequencies.pop("this", None)
    frequencies.pop("with", None)
    frequencies.pop("world bank", None)
    frequencies.pop("world bank group", None)

    # cloud = wordcloud.WordCloud(width=1920, height=1080,
    #                             background_color='white',
    #                             stopwords=stop_words.STOP_WORDS,
    #                             font_path="./assets/fonts/roboto/Roboto-Regular.ttf").generate(text)

    cloud = wordcloud.WordCloud(width=1920, height=1080,
                                background_color='white',
                                font_path="./assets/fonts/roboto/Roboto-Regular.ttf").generate_from_frequencies(
        frequencies)

    plt.imshow(cloud)
    plt.tight_layout(pad=0)
    plt.axis('off')
    plt.savefig(image_path, dpi=300, bbox_inches='tight')

    return frequencies

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Starting up word cloud generator")

    make_one_word_cloud("_portfolio/scaling_up_romania.txt",
                        "_portfolio/scaling_up_romania_word_cloud.png")

    make_one_word_cloud("_portfolio/starting_up_romania.txt",
                        "_portfolio/starting_up_romania_word_cloud.png")

    frequencies = make_one_word_cloud(
        "_portfolio/digital_entrepreneurship_and_innovation_in_central_america.txt",
        "_portfolio/digital_entrepreneurship_and_innovation_in_central_america_word_cloud.png")

    sorted_frequencies = dict(sorted(frequencies.items()))
