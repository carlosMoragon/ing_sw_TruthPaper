import unittest
from ..modules import classes as cl, web_scrapping as ws, DBManager as manager


class TestWebScrapping(unittest.TestCase):
    def test_get_news(self):
        news = ws.get_news()


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
    