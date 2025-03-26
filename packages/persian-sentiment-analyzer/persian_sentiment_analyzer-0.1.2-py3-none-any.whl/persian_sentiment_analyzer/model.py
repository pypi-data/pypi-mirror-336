import numpy as np
import pickle
import os
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from .preprocessor import TextPreprocessor

class SentimentAnalyzer:
    def __init__(self, model_path=None):
        self.preprocessor = TextPreprocessor()
        self.word2vec_model = None
        self.classifier = LogisticRegression(max_iter=1000)
        self.vector_size = 100
        
        if model_path:
            self.load_model(model_path)
    
    def train_word2vec(self, sentences, **kwargs):
        self.word2vec_model = Word2Vec(
            sentences=sentences,
            vector_size=kwargs.get('vector_size', 100),
            window=kwargs.get('window', 5),
            min_count=kwargs.get('min_count', 1),
            workers=kwargs.get('workers', 4)
        )
        self.vector_size = self.word2vec_model.vector_size
    
    def sentence_vector(self, sentence):
        if not self.word2vec_model:
            raise ValueError("Word2Vec model is not initialized")
        
        vectors = [
            self.word2vec_model.wv[word] 
            if word in self.word2vec_model.wv else np.zeros(self.vector_size)
            for word in sentence
        ]
        return np.mean(vectors, axis=0) if vectors else np.zeros(self.vector_size)
    
    def train_classifier(self, X, y):
        self.classifier.fit(X, y)
    
    def predict(self, text):
        tokens = self.preprocessor.preprocess_text(text)
        vector = self.sentence_vector(tokens)
        return self._map_label(self.classifier.predict([vector])[0])
    
    def _map_label(self, label):
        return {0: 'not_recommended', 1: 'recommended', 2: 'no_idea'}.get(label, 'no_idea')
    
    def save_model(self, path):
        os.makedirs(path, exist_ok=True)
        self.word2vec_model.save(os.path.join(path, "word2vec.model"))
        with open(os.path.join(path, "classifier.pkl"), 'wb') as f:
            pickle.dump(self.classifier, f)
    
    def load_model(self, path):
        self.word2vec_model = Word2Vec.load(os.path.join(path, "word2vec.model"))
        with open(os.path.join(path, "classifier.pkl"), 'rb') as f:
            self.classifier = pickle.load(f)
        self.vector_size = self.word2vec_model.vector_size
