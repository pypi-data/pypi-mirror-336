import numpy as np
import pickle
import os
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from .preprocessor import TextPreprocessor

class SentimentAnalyzer:
    def __init__(self, model_path=None):
        """
        Initialize the Sentiment Analyzer
        
        Args:
            model_path (str, optional): Path to a pre-trained model. Defaults to None.
        """
        self.preprocessor = TextPreprocessor()
        self.word2vec_model = None
        self.classifier = LogisticRegression(max_iter=1000)
        self.vector_size = 100  # Default vector size
        
        if model_path:
            self.load_model(model_path)
    
    def train_word2vec(self, sentences, vector_size=100, window=5, min_count=1, workers=4):
        """
        Train Word2Vec model on given sentences
        
        Args:
            sentences (list): List of tokenized sentences
            vector_size (int, optional): Dimension of word vectors. Defaults to 100.
            window (int, optional): Maximum distance between current and predicted word. Defaults to 5.
            min_count (int, optional): Ignores words with frequency lower than this. Defaults to 1.
            workers (int, optional): Number of worker threads. Defaults to 4.
        """
        self.vector_size = vector_size
        self.word2vec_model = Word2Vec(
            sentences=sentences,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            workers=workers
        )
    
    def sentence_vector(self, sentence):
        """
        Convert a sentence to its vector representation by averaging word vectors
        
        Args:
            sentence (list): Tokenized sentence
            
        Returns:
            numpy.ndarray: Sentence vector
        """
        if self.word2vec_model is None:
            raise ValueError("Word2Vec model is not trained or loaded")
            
        vectors = []
        for word in sentence:
            try:
                vectors.append(self.word2vec_model.wv[word])
            except KeyError:
                vectors.append(np.zeros(self.word2vec_model.vector_size))
        
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(self.word2vec_model.vector_size)
    
    def train_classifier(self, X, y):
        """
        Train the logistic regression classifier
        
        Args:
            X (numpy.ndarray): Feature vectors
            y (numpy.ndarray): Target labels
        """
        if self.word2vec_model is None:
            raise ValueError("Word2Vec model must be trained or loaded first")
            
        self.classifier.fit(X, y)
    
    def predict(self, text):
        """
        Predict sentiment of a given text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            str: Predicted sentiment ('recommended', 'not_recommended', or 'no_idea')
        """
        if self.word2vec_model is None or self.classifier is None:
            raise ValueError("Model must be trained or loaded before prediction")
            
        preprocessed = self.preprocessor.preprocess_text(text)
        vector = self.sentence_vector(preprocessed)
        prediction = self.classifier.predict([vector])[0]
        
        if prediction == 2:
            return "no_idea"
        elif prediction == 1:
            return "recommended"
        else:
            return "not_recommended"
    
    def save_model(self, path):
        """
        Save the trained models to disk
        
        Args:
            path (str): Directory path to save the models
        """
        if not os.path.exists(path):
            os.makedirs(path)
            
        # Save Word2Vec model
        if self.word2vec_model:
            word2vec_path = os.path.join(path, "word2vec.model")
            self.word2vec_model.save(word2vec_path)
        
        # Save classifier
        classifier_path = os.path.join(path, "classifier.pkl")
        with open(classifier_path, 'wb') as f:
            pickle.dump(self.classifier, f)
        
        # Save vector size
        meta_path = os.path.join(path, "meta.pkl")
        with open(meta_path, 'wb') as f:
            pickle.dump({'vector_size': self.vector_size}, f)
    
    def load_model(self, path):
        """
        Load trained models from disk
        
        Args:
            path (str): Directory path containing the saved models
        """
        # Load Word2Vec model
        word2vec_path = os.path.join(path, "word2vec.model")
        if os.path.exists(word2vec_path):
            self.word2vec_model = Word2Vec.load(word2vec_path)
        else:
            raise FileNotFoundError(f"Word2Vec model not found at {word2vec_path}")
        
        # Load classifier
        classifier_path = os.path.join(path, "classifier.pkl")
        if os.path.exists(classifier_path):
            with open(classifier_path, 'rb') as f:
                self.classifier = pickle.load(f)
        else:
            raise FileNotFoundError(f"Classifier model not found at {classifier_path}")
        
        # Load meta data
        meta_path = os.path.join(path, "meta.pkl")
        if os.path.exists(meta_path):
            with open(meta_path, 'rb') as f:
                meta = pickle.load(f)
                self.vector_size = meta.get('vector_size', 100)
        else:
            self.vector_size = 100  # Default value if meta not found