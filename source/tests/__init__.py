import unittest
from modules import classes as cl, webScrapping as ws
class TestClasses(unittest.TestCase):
    def test_news(self):
        self.assertEquals(cl.News("titulo", "imagen", "resumen", "url", ["que guay", "hola", "que tal"], "2023-12-01", ),)
