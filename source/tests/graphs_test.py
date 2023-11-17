import unittest
# from modules import  graphs
# from ..modules/graphs import graph_news_per_source, graph_news_per_category, wordcloud_per_category, get_categories
from ..modules.classes import News
from ..modules.graphs import graph_news_per_source, graph_news_per_category, wordcloud_per_category, get_categories

class TestGraphFunctions(unittest.TestCase):

    def test_graph_news_per_source(self):
        # Crea una lista de noticias para probar la función
        news = [News(owner="Source1", category="Category1", content="Content1"),
                News(owner="Source2", category="Category2", content="Content2"),
                News(owner="Source1", category="Category3", content="Content3")]

        # Llama a la función y verifica que no haya errores
        try:
            graph_news_per_source(news)
        except Exception as e:
            self.fail(f"La función graph_news_per_source generó un error: {e}")

    def test_graph_news_per_category(self):
        # Crea una lista de noticias para probar la función
        news = [News(owner="Source1", category="Category1", content="Content1"),
                News(owner="Source2", category="Category2", content="Content2"),
                News(owner="Source1", category="Category3", content="Content3")]

        # Llama a la función y verifica que no haya errores
        try:
            graph_news_per_category(news)
        except Exception as e:
            self.fail(f"La función graph_news_per_category generó un error: {e}")

    def test_wordcloud_per_category(self):
        # Crea una lista de noticias para probar la función
        news = [News(owner="Source1", category="Category1", content="Content1"),
                News(owner="Source2", category="Category1", content="Content2"),
                News(owner="Source1", category="Category2", content="Content3")]

        # Llama a la función y verifica que no haya errores
        try:
            wordcloud_per_category(news, "Category1")
        except Exception as e:
            self.fail(f"La función wordcloud_per_category generó un error: {e}")

    def test_get_categories(self):
        # Crea una lista de noticias para probar la función
        news = [News(owner="Source1", category="Category1", content="Content1"),
                News(owner="Source2", category="Category2", content="Content2"),
                News(owner="Source1", category="Category1", content="Content3")]

        # Llama a la función y verifica que devuelva las categorías correctas
        expected_result = ["Category1", "Category2"]
        result = get_categories(news)
        self.assertListEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
