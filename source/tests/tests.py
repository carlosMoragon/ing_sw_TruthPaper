import unittest
from ..modules import classes as cl, web_scrapping as ws, DBManager as manager


class TestWebScrapping(unittest.TestCase):
    def test_clasify_news(self):
        news_list = [
            cl.News(id=1, owner='owner1', title='Title 1', image='image1', url='url1', content='content1',
                 journalist=1, date='2023-01-01', category='Category 1', likes=10, views=100, container_id=-1),
            cl.News(id=2, owner='owner1', title='Title 2', image='image2', url='url2', content='content2',
                 journalist=2, date='2023-01-02', category='Category 1', likes=20, views=200, container_id=-1),
            cl.News(id=3, owner='owner1', title='Title 3', image='image3', url='url3', content='content3',
                 journalist=3, date='2023-01-03', category='Category 2', likes=30, views=300, container_id=-1),
            cl.News(id=4, owner='owner2', title='Title 4', image='image4', url='url4', content='content4',
                 journalist=4, date='2023-01-04', category='Category 2', likes=40, views=400, container_id=-1),
            cl.News(id=5, owner='owner2', title='Title 5', image='image5', url='url5', content='content5',
                 journalist=5, date='2023-01-05', category='Category 3', likes=50, views=500, container_id=-1),
            cl.News(id=6, owner='owner2', title='Title 6', image='image6', url='url6', content='content6',
                 journalist=6, date='2023-01-06', category='Category 3', likes=60, views=600, container_id=-1),
            cl.News(id=7, owner='owner3', title='Title 7', image='image7', url='url7', content='content7',
                 journalist=7, date='2023-01-07', category='Category 3', likes=70, views=700, container_id=-1)
        ]

        updated_news = ws.add_new_container(news_list, app=None)

        self.assertNotEqual(updated_news[0].get_container_id(), -1)
        self.assertEqual(updated_news[0].get_container_id(), updated_news[1].get_container_id())
        self.assertNotEqual(updated_news[1].get_container_id(), -1)

    def test_clasify_news_same_content(self):
        news_list = [
            cl.News(id=1, owner='owner1', title='Title 1', image='image1', url='url1', content='content1',
                 journalist=1, date='2023-01-01', category='Category 1', likes=10, views=100, container_id=-1),
            cl.News(id=2, owner='owner1', title='Title 2', image='image2', url='url2', content='content2',
                 journalist=2, date='2023-01-02', category='Category 1', likes=20, views=200, container_id=-1),
        ]
         
        news_list[0].set_content("ESTE CONTENIDO ES EL MISMO.")
        news_list[1].set_content("ESTE CONTENIDO ES EL MISMO.")

        updated_news = ws.add_new_container(news_list, app=None)

        self.assertEqual(updated_news[0].get_container_id(), updated_news[1].get_container_id())

    def test_clasify_news_diferent_content(self):
        news_list = [
            cl.News(id=1, owner='owner1', title='Title 1', image='image1', url='url1', content='content1',
                 journalist=1, date='2023-01-01', category='Category 1', likes=10, views=100, container_id=-1),
            cl.News(id=2, owner='owner1', title='Title 2', image='image2', url='url2', content='content2',
                 journalist=2, date='2023-01-02', category='Category 1', likes=20, views=200, container_id=-1),
        ]
         
        news_list[0].set_content("Abdul se comia una fresa con nata mientras andaba visitando Caceres.")
        news_list[1].set_content("Sebastian era el rey de los albaricoques, hasta que un día se enamoro de Paco.")

        updated_news = ws.add_new_container(news_list, app=None)

        self.assertNotEqual(updated_news[0].get_container_id(), updated_news[1].get_container_id())

    def test_clasify_news_diferent_content(self):
        news_list = [
            cl.News(id=1, owner='owner1', title='Title 1', image='image1', url='url1', content='content1',
                 journalist=1, date='2023-01-01', category='Category 1', likes=10, views=100, container_id=-1),
            cl.News(id=2, owner='owner1', title='Title 2', image='image2', url='url2', content='content2',
                 journalist=2, date='2023-01-02', category='Category 1', likes=20, views=200, container_id=-1),
            cl.News(id=3, owner='owner1', title='Title 3', image='image3', url='url3', content='content3',
                 journalist=3, date='2023-01-03', category='Category 2', likes=30, views=300, container_id=-1),
            cl.News(id=4, owner='owner2', title='Title 4', image='image4', url='url4', content='content4',
                 journalist=4, date='2023-01-04', category='Category 2', likes=40, views=400, container_id=-1),
            cl.News(id=5, owner='owner2', title='Title 5', image='image5', url='url5', content='content5',
                 journalist=5, date='2023-01-05', category='Category 3', likes=50, views=500, container_id=-1),
            cl.News(id=6, owner='owner2', title='Title 6', image='image6', url='url6', content='content6',
                 journalist=6, date='2023-01-06', category='Category 3', likes=60, views=600, container_id=-1),
            cl.News(id=7, owner='owner3', title='Title 7', image='image7', url='url7', content='content7',
                 journalist=7, date='2023-01-07', category='Category 3', likes=70, views=700, container_id=-1)
        ]
         
        news_list[0].set_content("Abdul se comia una fresa con nata mientras andaba visitando Caceres.")
        news_list[2].set_content("Conoce conmigo a Abdul, la persona que por comer fresas con nata por Caceres, desencadeno una guerra")
        news_list[1].set_content("El amor lo vence todo, Paco cambia al rey de los albaricoques")
        news_list[3].set_content("Sebastian era el rey de los albaricoques, hasta que un dia se enamoro de Paco.")
        news_list[4].set_content("Juan se pone celoso, Sebastian se va con Paco ,y lo deja atras con sus albaricoques")
    

        updated_news = ws.add_new_container(news_list, app=None)

        self.assertTrue(updated_news[1].get_container_id() == updated_news[3].get_container_id() and updated_news[3].get_container_id() == updated_news[4].get_container_id())
        self.assertTrue(updated_news[0].get_container_id() == updated_news[2].get_container_id())


    

class TestVerificationAlgorithms(unittest.TestCase):
    def test_verification_date_good(self):
        self.assertEqual(cl.validate_date("2023-11-19"), True)

    def test_verification_date_bad_1(self):
        self.assertEqual(cl.validate_date("19-2023-11"), False)

    def test_verification_date_bad_2(self):
        self.assertEqual(cl.validate_date("19-11-2023"), False)

    def test_verification_date_bad_string(self):
        self.assertEqual(cl.validate_date("aaaaaaaaa"), False)

    def test_verification_date_bad_3(self):
        self.assertEqual(cl.validate_date("2023/11/19"), False)


    def test_verification_password_good(self):
        self.assertEqual(cl.validate_password("Holamundo1234@"), True)

    def test_verification_password_bad_only_ints(self):
        self.assertEqual(cl.validate_password("1234"), False)

    def test_verification_password_bad_no_special_caracter(self):
        self.assertEqual(cl.validate_password("HolaMundo1234"), False)

    def test_verification_password_bad_no_ints(self):
        self.assertEqual(cl.validate_password("HolaMundo@"), False)

    def test_verification_password_bad_3_ints(self):
        self.assertEqual(cl.validate_password("HolaMundo123@"), False)

    def test_verification_password_bad_no_capital_letter(self):    
        self.assertEqual(cl.validate_password("molamundo1234@"), False)

    def test_verification_email_good(self):
        self.assertEqual(cl.validate_email("email@dominio.com"), True)

    def test_verification_email_bad_1(self):
        self.assertEqual(cl.validate_email("email"), False)

    def test_verification_email_bad_2(self):
        self.assertEqual(cl.validate_email("email@dominio"), False)

    def test_verification_email_bad_3(self):
        self.assertEqual(cl.validate_email("email@dominio."), False)

    def test_verification_email_bad_4(self):
        self.assertEqual(cl.validate_email("email@.com"), False)

    def test_verification_email_bad_5(self):
        self.assertEqual(cl.validate_email("email@dominio..com"), False)

    def test_verification_email_bad_6(self):
        self.assertEqual(cl.validate_email("email@@dominio.com"), False)

    def test_verification_email_bad_7(self):
        self.assertEqual(cl.validate_email("email@."), False)

    def test_verification_email_bad_8(self):
        self.assertEqual(cl.validate_email("@dominio.com"), False)

    def test_verification_email_bad_9(self):
        self.assertEqual(cl.validate_email("email@dominio.c"), False)

    def test_verification_email_bad_10(self):
        self.assertEqual(cl.validate_email(""), False)


# class TestUserLogIn(unittest.TestCase):
#     def test_login(self):
#         #1. Se toman los datos del form en el html
#         respuesta_login = manager.login('AgentMobius', 'Jetskis1111*') 
#         #2. Con esos datos se lanza una consulta a la base de datos
#         #3. Se comprueba que el usuario existe
#         self.assertEqual(respuesta_login, True) 
    
# class TestUserCreation(unittest.TestCase):
#     #1. Se hace un log in
#         # 1.1 Si el log in, tiene exito, se llama a un mapper que trae los datos de un usuario 
#         # 1.2 El objeto usuario se crea con esos datos
#     def testCreaacionUsuario(self):
#         respuesta_login = True
#         nombre_usuario = 'AgentMobius' #Lo sacará del form
#         user_data = usermapper.getAllUserData(nombre_usuario) 
#         nuevo_usuario = User(user_data)
        
    # Un usuario se loggea con exito
    #2. Partiendo de sus datos en la bbdd, se crea un usuario en la app (ESTO LO HACE EL MAPPER)
    