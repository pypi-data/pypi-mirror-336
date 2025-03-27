import unittest
from PerSent.core.analyzer import PersianSentimentAnalyzer
from PerSent.domains import NewsAnalyzer

class TestCoreFunctionality(unittest.TestCase):
    def setUp(self):
        self.general_analyzer = PersianSentimentAnalyzer()
        self.news_analyzer = NewsAnalyzer()

    def test_general_analysis(self):
        result = self.general_analyzer.analyze("این محصول خوب است")
        self.assertIn(result, ['positive', 'negative', 'neutral'])

    def test_news_analysis(self):
        news_text = "رشد اقتصادی در سال جاری مثبت بود"
        result = self.news_analyzer.analyze(news_text)
        self.assertEqual(result, 'positive')

if __name__ == '__main__':
    unittest.main()