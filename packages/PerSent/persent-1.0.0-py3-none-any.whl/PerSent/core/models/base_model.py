import joblib
import numpy as np
from gensim.models import Word2Vec
from typing import List

class BaseModel:
    def __init__(self, model_path: str = None):
        self.vectorizer = None
        self.classifier = None
        if model_path:
            self.load(model_path)

    def predict(self, tokens: List[str]) -> str:
        """پیش‌بینی احساس از توکن‌ها"""
        vector = self._vectorize(tokens)
        pred = self.classifier.predict([vector])[0]
        return self._decode_prediction(pred)

    def _vectorize(self, tokens: List[str]) -> np.ndarray:
        """تبدیل توکن‌ها به بردار"""
        vectors = [self.vectorizer.wv[t] for t in tokens if t in self.vectorizer.wv]
        return np.mean(vectors, axis=0) if vectors else np.zeros(100)

    def _decode_prediction(self, code: int) -> str:
        """تبدیل کد پیش‌بینی به متن"""
        return {0: 'negative', 1: 'positive', 2: 'neutral'}.get(code, 'neutral')

    def load(self, model_dir: str):
        """بارگذاری مدل از مسیر"""
        self.vectorizer = Word2Vec.load(f"{model_dir}/word2vec.model")
        self.classifier = joblib.load(f"{model_dir}/classifier.joblib")