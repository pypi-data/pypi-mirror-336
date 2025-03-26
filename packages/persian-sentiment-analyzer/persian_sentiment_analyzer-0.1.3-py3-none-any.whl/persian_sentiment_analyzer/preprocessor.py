from hazm import Normalizer, word_tokenize, Stemmer
from hazm.utils import stopwords_list
import re

class TextPreprocessor:
    def __init__(self):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
    
    def preprocess_text(self, text):
        """پردازش کامل متن فارسی"""
        text = self.normalizer.normalize(str(text))
        text = re.sub(r'[\d۰-۹]+', '', text)  # حذف اعداد
        text = re.sub(r'[!()\-\[\]{};:\'"<>?@#$%^&*_~]', ' ', text)  # حذف علائم
        tokens = word_tokenize(text)
        return [
            self.stemmer.stem(token)
            for token in tokens
            if token not in self.stopwords and len(token) > 1
        ]
