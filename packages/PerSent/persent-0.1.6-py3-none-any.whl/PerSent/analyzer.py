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
from transformers import pipeline
import torch
from torch.nn.functional import softmax

class AdvancedPersianSentimentAnalyzer:
    def __init__(self, model_dir='persian_sentiment/model'):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
        self.model_dir = model_dir
        self.vectorizer = None
        self.classifier = None
        
        # تنظیمات پیشرفته برای مدل احساسات
        self.emotion_analyzer = pipeline(
            "text-classification",
            model="HooshvareLab/bert-fa-base-uncased-emotion",
            tokenizer="HooshvareLab/bert-fa-base-uncased-emotion",
            device=0 if torch.cuda.is_available() else -1,
            return_all_scores=True
        )
        
        # پارامترهای بهینه شده
        self.w2v_params = {
            'vector_size': 300,
            'window': 10,
            'min_count': 2,
            'workers': 4,
            'sg': 1  # استفاده از skip-gram
        }
        
        # نگاشت برچسب‌های احساسات
        self.emotion_labels = {
            'ترس': 'Fear',
            'تعجب': 'Surprise',
            'خشم': 'Anger',
            'تحقیر': 'Contempt',
            'شادی': 'Joy',
            'غم': 'Sadness',
            'انزجار': 'Disgust'
        }
        
        os.makedirs(self.model_dir, exist_ok=True)

    def _preprocess_text(self, text, for_emotion=False):
        """پیش‌پردازش متن با قابلیت تنظیم برای تحلیل احساسات"""
        text = self.normalizer.normalize(str(text))
        
        if for_emotion:
            # حفظ علائم نگارشی برای تحلیل احساسات
            text = re.sub(r'[۰-۹\d]+', ' ', text)
        else:
            text = re.sub(r'[!()-\[\]{};:\'",؟<>./?@#$%^&*_~۰-۹\d]+', ' ', text)
            
        text = re.sub(r'\s+', ' ', text).strip()
        
        if not for_emotion:
            tokens = word_tokenize(text)
            return [
                self.stemmer.stem(token)
                for token in tokens
                if token not in self.stopwords and len(token) > 1
            ]
        return text

    def _sentence_vector(self, sentence, model):
        """تبدیل جمله به بردار با میانگین وزنی"""
        vectors = []
        weights = []
        
        for word in sentence:
            try:
                vectors.append(model.wv[word])
                # وزن‌دهی بر اساس فرکانس کلمه
                weights.append(model.wv.get_vecattr(word, "count"))
            except KeyError:
                continue
                
        if vectors:
            weights = np.array(weights) / sum(weights)
            return np.average(vectors, axis=0, weights=weights)
        return np.zeros(self.w2v_params['vector_size'])

    def _emotion_analysis(self, text):
        """تحلیل احساسات پیشرفته با مدل BERT"""
        try:
            # پیش‌پردازش متن برای تحلیل احساسات
            processed_text = self._preprocess_text(text, for_emotion=True)
            
            # تحلیل احساسات
            results = self.emotion_analyzer(processed_text)[0]
            
            # پردازش نتایج
            emotions = {}
            for item in results:
                fa_label = item['label']
                if fa_label in self.emotion_labels:
                    en_label = self.emotion_labels[fa_label]
                    score = round(float(item['score']), 4)
                    emotions[en_label] = score
            
            # اگر همه مقادیر صفر بودند، قوی‌ترین احساس را برگردان
            if all(v == 0 for v in emotions.values()) and results:
                top_emotion = max(results, key=lambda x: x['score'])
                fa_label = top_emotion['label']
                if fa_label in self.emotion_labels:
                    en_label = self.emotion_labels[fa_label]
                    emotions[en_label] = round(float(top_emotion['score']), 4)
            
            return emotions
            
        except Exception as e:
            print(f"خطا در تحلیل احساسات: {str(e)}")
            return {label: 0.0 for label in self.emotion_labels.values()}

    def train(self, train_csv, test_size=0.2):
        """آموزش پیشرفته مدل تحلیل توصیه"""
        df = pd.read_csv(train_csv)
        
        # تعادل کلاس‌ها
        class_counts = df['recommendation_status'].value_counts()
        max_samples = class_counts.max()
        balanced_df = pd.concat([
            df[df['recommendation_status'] == cls].sample(max_samples, replace=True)
            for cls in class_counts.index
        ])
        
        balanced_df['tokens'] = balanced_df['body'].progress_apply(
            lambda x: self._preprocess_text(x))
        
        # آموزش مدل Word2Vec با پارامترهای بهینه
        self.vectorizer = Word2Vec(
            sentences=balanced_df['tokens'],
            **self.w2v_params
        )
        
        # استخراج ویژگی‌های پیشرفته
        X = np.array([self._sentence_vector(s, self.vectorizer) 
                     for s in tqdm(balanced_df['tokens'], desc="Vectorizing")])
        y = balanced_df['recommendation_status'].map({
            "no_idea": 2,
            "recommended": 1,
            "not_recommended": 0
        }).values
        
        # تقسیم داده‌ها با stratify
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y)
        
        # مدل طبقه‌بندی با تنظیمات بهینه
        self.classifier = LogisticRegression(
            max_iter=2000,
            class_weight='balanced',
            C=0.5,
            solver='saga'
        )
        self.classifier.fit(X_train, y_train)
        
        # ذخیره مدل
        self.save_model()
        
        # ارزیابی دقیق‌تر
        train_acc = self.classifier.score(X_train, y_train)
        test_acc = self.classifier.score(X_test, y_test)
        
        return {
            'train_accuracy': round(train_acc, 4),
            'test_accuracy': round(test_acc, 4),
            'model_params': self.w2v_params
        }

    def predict(self, text, mode=0, threshold=0.1):
        """
        پیش‌بینی پیشرفته با قابلیت تنظیم آستانه
        
        پارامترها:
            text (str): متن ورودی
            mode (int): حالت تحلیل (0=توصیه، 1=احساسات)
            threshold (float): آستانه اطمینان برای تحلیل احساسات
            
        بازگشتی:
            dict یا str: نتایج تحلیل
        """
        if mode == 1:
            emotions = self._emotion_analysis(text)
            # فیلتر کردن احساسات با احتمال پایین
            return {
                k: v for k, v in emotions.items() 
                if v >= threshold
            }
            
        if not self.classifier or not self.vectorizer:
            raise Exception("Model not trained! Call train() first.")
            
        tokens = self._preprocess_text(text)
        vector = self._sentence_vector(tokens, self.vectorizer)
        proba = self.classifier.predict_proba([vector])[0]
        
        # تصمیم‌گیری با در نظر گرفتن احتمال
        if max(proba) < 0.6:  # آستانه اطمینان
            return "no_idea"
            
        prediction = self.classifier.predict([vector])[0]
        return {
            0: "not_recommended",
            1: "recommended",
            2: "no_idea"
        }[prediction]

    def save_model(self):
        """ذخیره مدل با نسخه‌بندی"""
        version = 1
        while os.path.exists(os.path.join(self.model_dir, f'classifier_v{version}.joblib')):
            version += 1
            
        joblib.dump(
            self.classifier, 
            os.path.join(self.model_dir, f'classifier_v{version}.joblib')
        )
        self.vectorizer.save(
            os.path.join(self.model_dir, f'word2vec_v{version}.model')
        )

    def load_model(self, version=None):
        """بارگذاری مدل با قابلیت انتخاب نسخه"""
        if version is None:
            versions = [
                int(f.split('_v')[-1].split('.')[0])
                for f in os.listdir(self.model_dir) 
                if f.startswith('classifier_v')
            ]
            version = max(versions) if versions else None
            
        if version:
            self.classifier = joblib.load(
                os.path.join(self.model_dir, f'classifier_v{version}.joblib')
            )
            self.vectorizer = Word2Vec.load(
                os.path.join(self.model_dir, f'word2vec_v{version}.model')
            )

