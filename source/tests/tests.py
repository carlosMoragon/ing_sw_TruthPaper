import unittest
from ..modules import classes as cl, web_scrapping as ws
from bs4 import BeautifulSoup
from datetime import datetime

class TestWebScrapping(unittest.TestCase):
    def test_add_a_container(self):
        news1 = cl.News("El Pais", "Titulo1", "https://elpais.com", "https://elpais.com/imagen1", "Contenido1", "CONTENIDO 1", -1, 0,"2020-11-19", "Categoria1")
        news2 = cl.News("El Pais", "Titulo2", "https://elpais.com", "https://elpais.com/imagen2", "Contenido2", "CONTENIDO 2", -1, 0, "2020-11-19", "Categoria2")
        news3 = cl.News("El Pais", "Titulo3", "https://elpais.com", "https://elpais.com/imagen3", "Contenido3", "CONTENIDO 3", -1, 0, "2020-11-19", "Categoria3")

        news = ws.add_new_container([news1, news2, news3])
        for new in news:
            self.assertNotEqual(new.get_container(), -1)

    def test_add_at_the_same_container(self):
        news1 = cl.News("El Pais", "Titulo1", "https://elpais.com", "https://elpais.com/imagen1", "url1","La inusual llegada de Pedro Sánchez a la Moncloa a bordo de un vehículo que recuerda al Batmóvil despierta intriga y teorías sobre su posible identidad secreta como 'Batman' político.", -1, 0,"2020-11-19", "Categoria1")
        news2 = cl.News("El Pais", "Titulo2", "https://elpais.com", "https://elpais.com/imagen2", "url2", "Pedro Sánchez sorprende al llegar a la Moncloa en un vehículo inusual, dejando a todos con la incógnita de lo que vendrá a continuación en su mandato.", -1, 0,"2020-11-19", "Categoria2")

        news = ws.add_new_container([news1, news2])
        self.assertEqual(news[0].get_container(), news[1].get_container())

    def test_add_different_containers(self):
        news1 = cl.News("El Pais", "Titulo1", "https://elpais.com", "https://elpais.com/imagen1", "url1","La inusual llegada de Pedro Sánchez a la Moncloa a bordo de un vehículo que recuerda al Batmóvil despierta intriga y teorías sobre su posible identidad secreta como 'Batman' político.", -1, 0,"2020-11-19", "Categoria1")
        news2 = cl.News("El Pais", "Titulo2", "https://elpais.com", "https://elpais.com/imagen2", "url2", "Pedro Sánchez sorprende al llegar a la Moncloa en un vehículo inusual, dejando a todos con la incógnita de lo que vendrá a continuación en su mandato.", -1, 0,"2020-11-19", "Categoria2")
        news3 = cl.News("El Pais", "Titulo3", "https://elpais.com", "https://elpais.com/imagen3", "url3", "Pedro Sánchez, en medio de un caluroso día de verano, disfrutó de un helado de fresa mientras reflexionaba sobre los desafíos políticos y saboreaba momentos de dulce descanso.", -1, 0, "2020-11-19", "Categoria3")
        news4 = cl.News("El Pais", "Titulo4", "https://elpais.com", "https://elpais.com/imagen4", "url4", "En una jornada veraniega abrasadora, Pedro Sánchez se deleitó con un helado de fresa, aprovechando para reflexionar sobre los retos políticos mientras disfrutaba de un merecido y refrescante descanso.", -1, 0, "2020-11-19", "Categoria4")

        news = ws.add_new_container([news1, news2, news3, news4])

        self.assertEqual(news[2].get_container(), news[3].get_container())
        self.assertEqual(news[0].get_container(), news[1].get_container())
        self.assertNotEqual(news[0].get_container(), news[2].get_container())

    @unittest.skip("No utilizar")
    def test_get_antena3news(self):
        html = ('<html><article class="article article--media-side"><a itemprop="mainentityofpage" href="https://www.antena3.com/noticias/espana/psoe-sumar-cierran-acuerdo-reeditar-gobierno-coalicion_2023102465376049e8e7a500013d860c.html" data-mod="a3mod_traffic" data-traffic="" data-pixel="" class="article__media video"><span class="icon-play"></span><picture><source media="(min-width: 1024px)" srcset="https://fotografias.antena3.com/clipping/cmsimages01/2023/10/24/030FDC31-D755-4F14-BC17-C137887D9EF4/pedro-sanchez-yolanda-diaz_58.jpg?crop=1920,1089,x0,y0&amp;width=1000&amp;height=567&amp;optimize=low&amp;format=webply" width="1000" height="567"><source media="(min-width: 300px)" srcset="https://fotografias.antena3.com/clipping/cmsimages01/2023/10/24/030FDC31-D755-4F14-BC17-C137887D9EF4/pedro-sanchez-yolanda-diaz_60.jpg?crop=1920,1080,x0,y0&amp;width=640&amp;height=360&amp;optimize=low&amp;format=webply" width="640" height="360"><img loading="lazy" class="lazy" src="https://fotografias.antena3.com/clipping/cmsimages01/2023/10/24/030FDC31-D755-4F14-BC17-C137887D9EF4/pedro-sanchez-yolanda-diaz_57.jpg?crop=1920,1110,x0,y0&amp;width=1280&amp;height=740&amp;optimize=low&amp;format=webply" data-original="https://fotografias.antena3.com/clipping/cmsimages01/2023/10/24/030FDC31-D755-4F14-BC17-C137887D9EF4/pedro-sanchez-yolanda-diaz_57.jpg?crop=1920,1110,x0,y0&amp;width=1280&amp;height=740&amp;optimize=low&amp;format=webply" alt="Pedro Sánchez y Yolanda Díaz" width="1280" height="740"></picture></a><div class="article__body"><div class="article__content"><header class="article__header"><p class="article__tag"><a href="https://www.antena3.com/noticias/espana/psoe-sumar-cierran-acuerdo-reeditar-gobierno-coalicion_2023102465376049e8e7a500013d860c.html" data-mod="a3mod_traffic" data-traffic="" data-pixel="">INVESTIDURA</a></p><h2 class="article__title small"><a href="https://www.antena3.com/noticias/espana/psoe-sumar-cierran-acuerdo-reeditar-gobierno-coalicion_2023102465376049e8e7a500013d860c.html" title="PSOE y Sumar cierran un acuerdo para reeditar el Gobierno de coalición" data-mod="a3mod_traffic" data-traffic="" data-pixel="">PSOE y Sumar cierran un acuerdo para reeditar el Gobierno de coalición</a></h2></header></div></div></article></html>')
        fake_structure = BeautifulSoup(html, "lxml")

        news = ws._make_antena3news(fake_structure, "general", "2023-10-23")
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0].get_owner(), "antena3noticias")
        self.assertEqual(news[0].get_title(), "PSOE y Sumar cierran un acuerdo para reeditar el Gobierno de coalición")
        self.assertEqual(news[0].get_url(), "https://www.antena3.com/noticias/espana/psoe-sumar-cierran-acuerdo-reeditar-gobierno-coalicion_2023102465376049e8e7a500013d860c.html")
        self.assertEqual(news[0].get_image(), "https://fotografias.antena3.com/clipping/cmsimages01/2023/10/24/030FDC31-D755-4F14-BC17-C137887D9EF4/pedro-sanchez-yolanda-diaz_57.jpg?crop=1920,1110,x0,y0&width=1280&height=740&optimize=low&format=webply")
        self.assertEqual(news[0].get_content(), "")
        self.assertEqual(news[0].get_container(), -1)
        self.assertEqual(news[0].get_journalist(), -1)
        self.assertEqual(news[0].get_date(), "2023-10-23")
        self.assertEqual(news[0].get_category(), "general")

    @unittest.skip("No se puede hacer el test porque la estructura de la página ha cambiado")
    def test_get_la_sexta_news(self):
        self.assertEqual(True, False)

    @unittest.skip("No se puede hacer el test porque la estructura de la página ha cambiado")
    def test_get_marca_news(self):
        self.assertEqual(True, False)

    @unittest.skip("No se puede hacer el test porque la estructura de la página ha cambiado")
    def test_get_nytimes_news(self):
        self.assertEqual(True, False)


class TestVerificationAlgorithms(unittest.TestCase):
    def test_verification_date_good(self):
        self.assertEqual(cl.validate_date("2023-11-19"), True)

    def test_verification_date_bad(self):
        self.assertEqual(cl.validate_date("19-2023-11"), False)
        self.assertEqual(cl.validate_date("19-11-2023"), False)
        self.assertEqual(cl.validate_date("aaaaaaaaa"), False)
        self.assertEqual(cl.validate_date("2023/11/19"), False)

    def test_verification_password_good(self):
        self.assertEqual(cl.validate_password("Holamundo1234@"), True)

    def test_verification_password_bad(self):
        self.assertEqual(cl.validate_password("1234"), False)
        self.assertEqual(cl.validate_password("HolaMundo1234"), False)
        self.assertEqual(cl.validate_password("HolaMundo@"), False)
        self.assertEqual(cl.validate_password("HolaMundo123@"), False)
        self.assertEqual(cl.validate_password("molamundo1234@"), False)

    def test_verification_email_good(self):
        self.assertEqual(cl.validate_email("email@dominio.com"), True)

    def test_verification_email_bad(self):
        self.assertEqual(cl.validate_email("email"), False)
        self.assertEqual(cl.validate_email("email@dominio"), False)
        self.assertEqual(cl.validate_email("email@dominio."), False)
        self.assertEqual(cl.validate_email("email@.com"), False)
        self.assertEqual(cl.validate_email("email@dominio..com"), False)
        self.assertEqual(cl.validate_email("email@@dominio.com"), False)
        self.assertEqual(cl.validate_email("email@."), False)
        self.assertEqual(cl.validate_email("@dominio.com"), False)
        self.assertEqual(cl.validate_email("email@dominio.c"), False)
        self.assertEqual(cl.validate_email(""), False)
