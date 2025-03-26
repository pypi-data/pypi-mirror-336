import re
from hazm import Normalizer, word_tokenize, Stemmer

class TextPreprocessor:
    def __init__(self):
        self.stopwords = set(stopwords_list())
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.punctuations = r'[!()-\[\]{};:\'",؟<>./?@#$%^&*_~]'
        self.numbers_regex = r'[۰-۹\d]+'
        self.white_space = r'\s+'
    
    def preprocess_text(self, text):
        text = self.normalizer.normalize(str(text))
        text = re.sub(self.numbers_regex, '', text)
        text = re.sub(self.punctuations, ' ', text)
        text = re.sub(self.white_space, ' ', text).strip()
        
        tokens = word_tokenize(text)
        processed_tokens = [
            self.stemmer.stem(token)
            for token in tokens
            if token not in self.stopwords and token.strip()
        ]
        
        return processed_tokens