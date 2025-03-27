import os
import pandas as pd
import urllib.request
import nltk
import re
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
from nltk import pos_tag
import chardet

# ✅ Download necessary NLTK resources
nltk.download("punkt")
nltk.download("wordnet")

# ✅ GitHub Raw URL for dataset (CORRECTED)
DATASET_URL = "https://raw.githubusercontent.com/birdcoreone/NLP-python/master/twi_nlp/data/twi_words.csv"
DEFAULT_FILEPATH = "data/twi_words.csv"

def detect_encoding(filepath):
    """Detect file encoding to handle UTF-8 issues."""
    with open(filepath, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]

class TwiNLP:
    def __init__(self, filepath=None):
        """Initialize the Twi NLP module with an optional dataset."""
        if filepath is None:
            filepath = os.path.join(os.getcwd(), "data", "twi_words.csv")

        if not os.path.exists(filepath):
            try:
                urllib.request.urlretrieve(DATASET_URL, filepath)
            except urllib.error.HTTPError:
                pass  # No unnecessary prints
            except urllib.error.URLError:
                pass  # No unnecessary prints

        if not os.path.exists(filepath):
            self.df = None
            self.words = []
            self.translations = {}
            self.lemmatizer = WordNetLemmatizer()
            self.stemmer = PorterStemmer()
            return

        encoding = detect_encoding(filepath)
        self.df = pd.read_csv(filepath, encoding=encoding)
        self.words = self.df['Twi'].tolist()
        self.translations = dict(zip(self.df['Twi'], self.df['English']))
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()

    def translate(self, word):
        """Translate a Twi word to English."""
        # print("🔍 Checking Translation Dictionary:", self.translations)  # Debugging
        return self.translations.get(word, "Translation not found")


    def get_pos(self, word):
        """Automatically tag POS by first translating to English, then tagging with NLTK."""
        english_translation = self.translate(word)
        if english_translation == "Translation not found":
            return "POS not found"

        # Tokenize and POS tag using NLTK
        tokens = word_tokenize(english_translation)
        pos_tags = pos_tag(tokens)

        return pos_tags  # Returns a list of tuples [(word, POS tag)]


    def search(self, keyword):
        """Search for words containing the keyword."""
        return [word for word in self.words if keyword in word]

    def tokenize(self, text):
        """Basic tokenizer using NLTK."""
        return word_tokenize(text)

    def stem_and_lemmatize(self, twi_word):
        """Stem & Lemmatize a Twi word using English as an intermediary."""
        english_translation = self.translate(twi_word)

        if english_translation == "Translation not found":
            return {"Stemmed": "N/A", "Lemmatized": "N/A"}  # No translation found

        # ✅ Apply Stemming and Lemmatization
        stemmed = self.stemmer.stem(english_translation.lower())
        lemmatized = self.lemmatizer.lemmatize(english_translation.lower())

        # ✅ Reverse Mapping: Convert back to Twi (Only If It Exists)
        twi_equivalent = next((twi for twi, eng in self.translations.items() if eng.lower() == lemmatized), "No Twi equivalent")

        return {"Stemmed": stemmed, "Lemmatized": lemmatized, "Twi Equivalent": twi_equivalent}

    def load_dataset(self, filepath):
        """Allows users to load a dataset manually."""
        encoding = detect_encoding(filepath)
        self.df = pd.read_csv(filepath, encoding=encoding)
        self.words = self.df['Twi'].tolist()
        self.translations = dict(zip(self.df['Twi'], self.df['English']))
        # self.pos_tags = dict(zip(self.df['Twi'], self.df['POS']))

# ✅ Example Usage
# def main():
#   twi_nlp = TwiNLP()
#   print(twi_nlp.stem_and_lemmatize("Nokware"))

# if __name__ == "__main__":
#    main()
