import pandas as pd
from hazm import Normalizer, word_tokenize, Stemmer, stopwords_list
import re
from tqdm import tdqm
from gensim.models import Word2Vec
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
import joblib

class PersianSentimentAnalyzer:
    def __init__(self, model_dir='persian_sentiment/model'):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
        self.model_dir = model_dir
        self.vectorizer = None
        self.classifier = None
        self.emotion_keywords = {
            'Fear': ['ترس', 'وحشت', 'هراس'],
            'Surprise': ['تعجب', 'شگفت', 'حیرت'],
            'Anger': ['خشم', 'عصبانیت', 'خشونت'],
            'Contempt': ['تحقیر', 'توهین', 'حقارت'],
            'Joy': ['شادی', 'خوشحالی', 'خنده'],
            'Sadness': ['غم', 'اندوه', 'ناراحتی'],
            'Disgust': ['انزجار', 'تهوع', 'نفرت']
        }
        
        os.makedirs(self.model_dir, exist_ok=True)
        
    def _preprocess_text(self, text):
        text = self.normalizer.normalize(str(text))
        text = re.sub(r'[!()-\[\]{};:\'",؟<>./?@#$%^&*_~۰-۹\d]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        tokens = word_tokenize(text)
        processed_tokens = [
            self.stemmer.stem(token)
            for token in tokens
            if token not in self.stopwords and len(token) > 1
        ]
        return processed_tokens
    
    def _sentence_vector(self, sentence, model):
        vectors = []
        for word in sentence:
            try:
                vectors.append(model.wv[word])
            except KeyError:
                vectors.append(np.zeros(100))
        return np.mean(vectors, axis=0) if vectors else np.zeros(100)
    
    def _emotion_analysis(self, tokens):
        """تحلیل احساسات بر اساس کلیدواژه‌های از پیش تعریف شده"""
        emotions = {emotion: 0 for emotion in self.emotion_keywords.keys()}
        for word in tokens:
            for emotion, keywords in self.emotion_keywords.items():
                if word in keywords:
                    emotions[emotion] += 1
        return emotions
    
    def train(self, train_csv, test_size=0.2, vector_size=100, window=5):
        df = pd.read_csv(train_csv)
        df['tokens'] = df['body'].apply(self._preprocess_text)
        
        self.vectorizer = Word2Vec(
            sentences=df['tokens'],
            vector_size=vector_size,
            window=window,
            min_count=1,
            workers=4
        )
        
        X = np.array([self._sentence_vector(s, self.vectorizer) for s in df['tokens']])
        y = df['recommendation_status'].map({
            "no_idea": 2,
            "recommended": 1,
            "not_recommended": 0
        }).values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        
        self.classifier = LogisticRegression(max_iter=1000)
        self.classifier.fit(X_train, y_train)
        
        self.save_model()
        accuracy = self.classifier.score(X_test, y_test)
        return accuracy
    
    def predict(self, text, mode=0):
        """پیش‌بینی احساس متن با قابلیت انتخاب حالت تحلیل
        
        پارامترها:
            mode (int): 
                0 = تحلیل توصیه (پیش‌فرض)
                1 = تحلیل احساسات (Fear, Joy, etc.)
        """
        if not self.classifier or not self.vectorizer:
            raise Exception("Model not trained! Call train() first or load a pretrained model.")
            
        tokens = self._preprocess_text(text)
        
        if mode == 0:
            vector = self._sentence_vector(tokens, self.vectorizer)
            prediction = self.classifier.predict([vector])[0]
            return {
                0: "not_recommended",
                1: "recommended",
                2: "no_idea"
            }[prediction]
            
        elif mode == 1:
            return self._emotion_analysis(tokens)
            
        else:
            raise ValueError("Invalid mode. Use 0 (recommendation analysis) or 1 (emotion analysis)")
    
    def save_model(self):
        joblib.dump(self.classifier, os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer.save(os.path.join(self.model_dir, 'word2vec.model'))
    
    def load_model(self):
        self.classifier = joblib.load(os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer = Word2Vec.load(os.path.join(self.model_dir, 'word2vec.model'))
