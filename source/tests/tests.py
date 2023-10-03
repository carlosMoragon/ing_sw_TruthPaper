import unittest
from modules import classes as cl, web_scrapping as ws


class TestClasses(unittest.TestCase):
    def test_news_good(self):
        self.assertEqual(
            cl.News("titulo", "imagen", "resumen", "url", "2023-12-01", "CEU").__str__()
            , "title: titulo, image: imagen, summary: resumen, url: url, comments: [], date: 2023-12-01, qualification: 0, owner: CEU")

    def test_news_bad(self):
        self.assertNotEqual(None, None)

    def test_comments_good(self):
        # owner: str, text: str, date: str, imgs: []
        self.assertEqual(
            cl.Comment("owner", "text", "2023-12-01", ["que guay", "hola", "que tal"]).__str__()
            , "owner: owner, text: text, date: 2023-12-01, imgs: ['que guay', 'hola', 'que tal']")

    def test_comments_bad(self):
        self.assertNotEqual(None,None)


    def test_users_good(self):
        self.assertEqual(
            cl.User("username", "password", "email@gmail.com", "profile_name", "123456789")
            .__str__()
            , "username: username, password: password, email: email@gmail.com, profile_name: profile_name, phone_number: 123456789")

        self.assertEqual(
            cl.CommonUser("username", "password", "email2gmail.com", "profile_name", "123456789", ["terror", "Christmas"], False)
            .__str__()
            , "username: username, password: password, email: email@gmail.com, profile_name: profile_name, phone_number: 123456789, interest_themes: ['terror', 'Christmas'], iscertificate: False")

        self.assertEqual(
            cl.PremiumUser("username", "password", "email2gmail.com", "profile_name", "123456789", "banck_account")
            .__str__()
            , "username: username, password: password, email: email@gmail.com, profile_name: profile_name, phone_number: 123456789, banck_account: banck_account")

        self.assertEqual(
            cl.User("username", "password", "email2gmail.com", "profile_name", "123456789", "CEU")
            .__str__()
            , "username: username, password: password, email: email@gmail.com, profile_name: profile_name, phone_number: 123456789, company: company")

    def test_users_bad(self):
        self.assertNotEqual(None,None)


class TestWebScrapping(unittest.TestCase):
    def test_get_antena3news(self):
        antena3_news = ws.get_antena3news()
        self.assertIsInstance(antena3_news, list)
        self.assertTrue(len(antena3_news) > 0)
        for news in antena3_news:
            self.assertIsInstance(news, cl.News)
            self.assertIsNotNone(news.get_title())
            self.assertIsNotNone(news.get_image())
            self.assertIsNotNone(news.get_url())
            self.assertIsNotNone(news.get_date())
            self.assertEqual(news.get_owner(), 'antena3noticias')

    def test_get_lasextanews(self):
        lasexta_news = ws.get_lasextanews()
        self.assertIsInstance(lasexta_news, list)
        self.assertTrue(len(lasexta_news) > 0)
        for news in lasexta_news:
            self.assertIsInstance(news, cl.News)
            self.assertIsNotNone(news.get_title())
            self.assertIsNotNone(news.get_image())
            self.assertIsNotNone(news.get_url())
            self.assertIsNotNone(news.get_date())
            self.assertEqual(news.get_owner(), 'LaSexta')


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
