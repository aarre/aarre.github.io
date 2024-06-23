#!venv/bin/python3

import logging
import re
import sys

import matplotlib.pyplot as plt
import textblob
import wordcloud

import nltk
nltk.download('brown')
nltk.download('punkt')
nltk.download('words')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def case_insensitive_replace(string_to_replace, replacement_string, original_string):
    """
    Replace all instances of old_string with new_string in text regardless of case.

    :param string_to_replace: The original string.
    :type string_to_replace: str
    :param replacement_string: The new string.
    :type replacement_string: str
    :param original_string: The text in which to perform the replacement.
    :type original_string: str
    :return: The text after performing the replacement.
    :rtype: str

    See `https://stackoverflow.com/questions/919056/case-insensitive-replace`
    """
    return re.sub('(?i)' + re.escape(string_to_replace), lambda m: replacement_string, original_string)


# See https://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-list
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def case_insensitive_remove_values_from_list(the_list, value_to_remove):
    return [value for value in the_list if value.lower() != value_to_remove.lower()]


def write_string_to_file(the_string, filename):
    with open(filename, 'w') as f:
        f.write(the_string)


# Extract text from PDF
# pdfFileObj = open('_portfolio/scaling_up_romania.pdf', 'rb')
# pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
# text = ''
# for page in pdfReader.pages:
#     text += page.extractText()
# pdfFileObj.close()
# text = text.replace("\n-", "")

# Avoid text from PDFs, which is full of OCR garbage in many cases
with open('_portfolio/scaling_up_romania.txt', 'r') as file:
    text = file.read()
text = text.replace("\n", " ")
#text = text.translate(str.maketrans('', '', string.punctuation))  # Remove all punctuation
# Remove short words
' '.join(word for word in text.split() if len(word)>2)
# Remove possessives with curly quotes, which show up as their own words with space in them
text = case_insensitive_replace("’s","", text)
write_string_to_file(text, "original.txt")

# # Drop non-English words and "stem" (lemmatize)
# snow_stemmer = SnowballStemmer(language='english')
# words = set(nltk.corpus.words.words())
# text = " ".join(snow_stemmer.stem(w) for w in nltk.wordpunct_tokenize(text) if snow_stemmer.stem(w) in words)
# write_string_to_file(text, "english.txt")

# Remove consecutive duplicates
# See https://stackoverflow.com/questions/39237350/how-do-i-remove-consecutive-duplicates-from-a-list
#english_words = [k for k, g in itertools.groupby(english_words)]

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
#english_text = " ".join(english_words)
# english_text = text
# english_text = case_insensitive_replace("entrepreneurial", "entrepreneurship", english_text)
# english_text = case_insensitive_replace("instruments", "instrument", english_text)
# english_text = case_insensitive_replace("romanian", "romania", english_text)
# english_text = case_insensitive_replace("romania's", "romania", english_text)
# english_text = case_insensitive_replace("scores", "score", english_text)
# english_text = case_insensitive_replace("startups", "startup", english_text)

# Try to correct spelling
blob = textblob.blob.TextBlob(text)

#blob.correct() - too slow

# Do automated lemmatization
# singular_list = [word.lemmatize() for word in blob.words]
# singular_list = remove_values_from_list(singular_list, "wa")  # Somehow introduced by TextBlob
# singular_text = " ".join(singular_list)
# write_string_to_file(singular_text, "singular.txt")
# singular_blob = textblob.blob.TextBlob(singular_text)

# Get frequencies of noun phrases
frequencies = blob.np_counts

# Remove short words (again)
frequencies = {key:frequencies[key] for key in frequencies if len(key)>2}

# Remove distractors
frequencies.pop("figure", None)
frequencies.pop("number", None)
frequencies.pop("romania", None)
frequencies.pop("romanian", None)
frequencies.pop("source", None)
frequencies.pop("world bank", None)
frequencies.pop("world bank group", None)

cloud = wordcloud.WordCloud(width=1920, height=1080, background_color='white',
                            font_path="./assets/fonts/roboto/Roboto-Regular.ttf").generate_from_frequencies(frequencies)

plt.imshow(cloud)
plt.tight_layout(pad=0)
plt.axis('off')
plt.show()
