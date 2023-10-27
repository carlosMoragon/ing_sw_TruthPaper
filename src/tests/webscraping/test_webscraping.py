import unittest
from src.services import web_scraping as ws


class TestWebScraping(unittest.TestCase):
    def test_get_news(self):
        news = ws.get_news()
