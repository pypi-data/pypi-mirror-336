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
            return_all_scores=True,
            function_to_apply='sigmoid'  # اضافه کردن تابع فعال‌ساز مناسب
        )
        
        # پارامترهای بهینه شده
        self.w2v_params = {
            'vector_size': 300,
            'window': 10,
            'min_count': 2,
            'workers': 4,
            'sg': 1
        }
        
        # لیست برچسب‌های احساسات
        self.emotion_labels = [
            'Fear', 'Surprise', 'Anger', 
            'Contempt', 'Joy', 'Sadness', 'Disgust'
        ]
        
        os.makedirs(self.model_dir, exist_ok=True)

    def _preprocess_emotion_text(self, text):
        """پیش‌پردازش تخصصی برای تحلیل احساسات"""
        # نرمال‌سازی و حفظ ساختار احساسی
        text = self.normalizer.normalize(text)
        text = re.sub(r'([!?.]){2,}', r'\1', text)  # حذف تکرار علائم نگارشی
        text = re.sub(r'[۰-۹]', ' ', text)  # حذف اعداد
        return text.strip()

    def _emotion_analysis(self, text):
        """تحلیل احساسات با مدیریت خطا و تنظیمات پیشرفته"""
        try:
            # پیش‌پردازش متن
            processed_text = self._preprocess_emotion_text(text)
            
            if len(processed_text) < 3:  # بررسی متن کوتاه
                raise ValueError("متن ورودی بسیار کوتاه است")
            
            # تحلیل احساسات
            results = self.emotion_analyzer(processed_text, top_k=None)[0]
            
            # پردازش نتایج
            emotions = {}
            for item in results:
                label = item['label']
                score = item['score']
                if label == 'ترس': emotions['Fear'] = score
                elif label == 'تعجب': emotions['Surprise'] = score
                elif label == 'خشم': emotions['Anger'] = score
                elif label == 'تحقیر': emotions['Contempt'] = score
                elif label == 'شادی': emotions['Joy'] = score
                elif label == 'غم': emotions['Sadness'] = score
                elif label == 'انزجار': emotions['Disgust'] = score
            
            # نرمال‌سازی امتیازات
            total = sum(emotions.values())
            if total > 0:
                for k in emotions:
                    emotions[k] = round(emotions[k]/total, 4)
            
            # فیلتر کردن نتایج ضعیف
            filtered = {k: v for k, v in emotions.items() if v >= 0.1}
            
            return filtered if filtered else emotions
            
        except Exception as e:
            print(f"خطا در تحلیل احساسات: {str(e)}")
            return {label: 0.0 for label in self.emotion_labels}

    # بقیه متدها بدون تغییر (train, predict, save_model, load_model, ...)

# تست نمونه
if __name__ == "__main__":
    analyzer = AdvancedPersianSentimentAnalyzer()
    
    # تست با جملات نمونه
    test_texts = [
        "من واقعاً از این اتفاق خشمگین هستم! این غیرقابل قبوله",
        "چه روز شگفت‌انگیزی بود، واقعاً خوشحالم",
        "از دیدن این صحنه حالم به هم خورد، واقعاً منزجر کننده بود",
        "می‌ترسم این اتفاق دوباره تکرار بشه"
    ]
    
    for text in test_texts:
        print(f"\nمتن: {text}")
        emotions = analyzer._emotion_analysis(text)
        print("نتایج تحلیل احساسات:")
        for emotion, score in emotions.items():
            print(f"{emotion}: {score:.4f}")
