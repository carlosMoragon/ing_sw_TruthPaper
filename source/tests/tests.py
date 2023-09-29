import unittest
from modules import classes as cl, webScrapping as ws


class TestClasses(unittest.TestCase):
    def test_news(self):
        self.assertEquals(
            cl.News("titulo", "imagen", "resumen", "url", ["que guay", "hola", "que tal"], "2023-12-01", 4, "CEU")
            .__str__()
            , "title: titulo, image: imagen, summary: resumen, url: url, comments: ['que guay', 'hola', 'que tal'], date: 2023-12-01, qualification: 4, owner: CEU")

    def test_comments(self):
        # owner: str, text: str, date: str, imgs: []
        self.assertEquals(
            cl.News("titulo", "imagen", "resumen", "url", ["que guay", "hola", "que tal"], "2023-12-01", 4, "CEU")
            .__str__()
            , "title: titulo, image: imagen, summary: resumen, url: url, comments: ['que guay', 'hola', 'que tal'], date: 2023-12-01, qualification: 4, owner: CEU")