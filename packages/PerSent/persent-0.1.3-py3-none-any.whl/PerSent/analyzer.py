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
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from torch.nn.functional import softmax

class PersianSentimentAnalyzer:
    def __init__(self, model_dir='persian_sentiment/model'):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
        self.model_dir = model_dir
        self.vectorizer = None
        self.classifier = None
        
        # مدل تحلیل احساسات
        self.emotion_tokenizer = AutoTokenizer.from_pretrained(
            "HooshvareLab/bert-fa-base-uncased-emotion")
        self.emotion_model = AutoModelForSequenceClassification.from_pretrained(
            "HooshvareLab/bert-fa-base-uncased-emotion")
        self.emotion_labels = ['ترس', 'تعجب', 'خشم', 'تحقیر', 'شادی', 'غم', 'انزجار']
        
        os.makedirs(self.model_dir, exist_ok=True)

    def _preprocess_text(self, text):
        """پیش‌پردازش متن فارسی"""
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
        """تبدیل جمله به بردار با میانگین بردارهای کلمات"""
        vectors = []
        for word in sentence:
            try:
                vectors.append(model.wv[word])
            except KeyError:
                vectors.append(np.zeros(100))
        return np.mean(vectors, axis=0) if vectors else np.zeros(100)

    def _emotion_analysis(self, text):
        """تحلیل احساسات با مدل BERT فارسی"""
        inputs = self.emotion_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        
        with torch.no_grad():
            outputs = self.emotion_model(**inputs)
        
        probs = softmax(outputs.logits, dim=1)
        scores = probs.numpy()[0]
        
        return {
            label: round(float(score), 4)
            for label, score in zip(self.emotion_labels, scores)
        }

    def train(self, train_csv, test_size=0.2, vector_size=100, window=5):
        """آموزش مدل تحلیل توصیه"""
        df = pd.read_csv(train_csv)
        df['tokens'] = df['body'].apply(self._preprocess_text)
        
        # آموزش مدل Word2Vec
        self.vectorizer = Word2Vec(
            sentences=df['tokens'],
            vector_size=vector_size,
            window=window,
            min_count=1,
            workers=4
        )
        
        # تبدیل جملات به بردار
        X = np.array([self._sentence_vector(s, self.vectorizer) for s in df['tokens']])
        y = df['recommendation_status'].map({
            "no_idea": 2,
            "recommended": 1,
            "not_recommended": 0
        }).values
        
        # تقسیم داده‌ها و آموزش مدل
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        self.classifier = LogisticRegression(max_iter=1000)
        self.classifier.fit(X_train, y_train)
        
        # ذخیره مدل
        self.save_model()
        accuracy = self.classifier.score(X_test, y_test)
        return round(accuracy, 4)

    def predict(self, text, mode=0):
        """
        پیش‌بینی احساس متن
        
        پارامترها:
            text (str): متن ورودی
            mode (int): 
                0 = تحلیل توصیه (پیش‌فرض)
                1 = تحلیل احساسات با مدل BERT
                
        بازگشتی:
            dict یا str: نتایج تحلیل
        """
        if mode == 0:
            if not self.classifier or not self.vectorizer:
                raise Exception("Recommendation model not trained! Call train() first.")
                
            tokens = self._preprocess_text(text)
            vector = self._sentence_vector(tokens, self.vectorizer)
            prediction = self.classifier.predict([vector])[0]
            return {
                0: "not_recommended",
                1: "recommended",
                2: "no_idea"
            }[prediction]
            
        elif mode == 1:
            return self._emotion_analysis(text)
            
        else:
            raise ValueError("Invalid mode. Use 0 (recommendation) or 1 (emotion)")

    def save_model(self):
        """ذخیره مدل تحلیل توصیه"""
        joblib.dump(self.classifier, os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer.save(os.path.join(self.model_dir, 'word2vec.model'))

    def load_model(self):
        """بارگذاری مدل تحلیل توصیه"""
        self.classifier = joblib.load(os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer = Word2Vec.load(os.path.join(self.model_dir, 'word2vec.model'))
