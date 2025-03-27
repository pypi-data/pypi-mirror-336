#import necessary library
import pandas as pd
from hazm import Normalizer, word_tokenize, Stemmer, stopwords_list
import re
from tqdm import tqdm
from gensim.models import Word2Vec
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
import joblib

class CommentAnalyzer:
    def __init__(self, model_dir='PerSent/model'):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
        self.model_dir = model_dir
        self.vectorizer = None
        self.classifier = None
        
        # make /model Directory if not exist
        os.makedirs(self.model_dir, exist_ok=True)
        
    def _preprocess_text(self, text):
        """PreProcess Persian Text"""
        # Normalizing
        text = self.normalizer.normalize(str(text))
        
        # remove number and sign
        text = re.sub(r'[!()-\[\]{};:\'",؟<>./?@#$%^&*_~۰-۹\d]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # tokenize and stemming
        tokens = word_tokenize(text)
        processed_tokens = [
            self.stemmer.stem(token)
            for token in tokens
            if token not in self.stopwords and len(token) > 1
        ]
        
        return processed_tokens
    
    def _sentence_vector(self, sentence, model):
        """convert sentences to vector by word2vec model"""
        vectors = []
        for word in sentence:
            try:
                vectors.append(model.wv[word])
            except KeyError:
                vectors.append(np.zeros(100))
        return np.mean(vectors, axis=0) if vectors else np.zeros(100)
    
    def train(self, train_csv, test_size=0.2, vector_size=100, window=5):
        """Train model"""
        # read data
        df = pd.read_csv(train_csv)
        df['tokens'] = df['body'].apply(self._preprocess_text)
        
        # train Word2Vec model
        self.vectorizer = Word2Vec(
            sentences=df['tokens'],
            vector_size=vector_size,
            window=window,
            min_count=1,
            workers=4
        )
        
        # convert sentences to vector
        X = np.array([self._sentence_vector(s, self.vectorizer) for s in df['tokens']])
        y = df['recommendation_status'].map({
            "no_idea": 2,
            "recommended": 1,
            "not_recommended": 0
        }).values
        
        # make train and test data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

        self.classifier = LogisticRegression(max_iter=1000)
        self.classifier.fit(X_train, y_train)
        
        # save model
        self.save_model()
        
        # evaluation
        accuracy = self.classifier.score(X_test, y_test)
        return accuracy
    
    def predict(self, text):
        """Predict text sentiment"""
        if not self.classifier or not self.vectorizer:
            raise Exception("Model not trained! Call train() first or load a pretrained model.")
            
        tokens = self._preprocess_text(text)
        vector = self._sentence_vector(tokens, self.vectorizer)
        prediction = self.classifier.predict([vector])[0]
        
        return {
            0: "not_recommended",
            1: "recommended",
            2: "no_idea"
        }[prediction]
    
    def save_model(self):
        """save trained model"""
        joblib.dump(self.classifier, os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer.save(os.path.join(self.model_dir, 'word2vec.model'))
    
    def load_model(self):
        """reload from file"""
        self.classifier = joblib.load(os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer = Word2Vec.load(os.path.join(self.model_dir, 'word2vec.model'))
