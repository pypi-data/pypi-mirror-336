# -*- coding: utf-8 -*-
"""
PerSent - کتابخانه جامع تحلیل احساسات متن فارسی

نسخه: 1.0.0
"""

from .core.analyzer import PersianSentimentAnalyzer
from .domains.news import NewsAnalyzer
from .domains.social import SocialMediaAnalyzer
from .domains.comments import CommentAnalyzer
from .utils.dictionary import load_custom_dictionary

# تعریف نسخه
__version__ = "1.0.0"
__all__ = [
    'PersianSentimentAnalyzer',
    'NewsAnalyzer',
    'SocialMediaAnalyzer',
    'CommentAnalyzer',
    'load_custom_dictionary'
]

# تنظیمات اولیه
class Config:
    DEFAULT_MODEL_PATH = "models/v1/"
    ENABLE_LOGGING = True
    MAX_TEXT_LENGTH = 5000

    @classmethod
    def set_model_path(cls, path):
        cls.DEFAULT_MODEL_PATH = path

# بارگذاری خودکار مدل‌های پایه
try:
    from .core.models import BaseModel
    base_model = BaseModel()
except ImportError as e:
    import warnings
    warnings.warn(f"Failed to load base models: {str(e)}")

# فعال کردن لوگر پیش‌فرض
if Config.ENABLE_LOGGING:
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('PerSent')
    logger.info(f"PerSent v{__version__} initialized")