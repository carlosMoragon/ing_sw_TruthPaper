import unittest
from ..database import DBManager as manager
from ..modules import  usermappers

class testUpdateUsers(unittest.TestCase):
    def setUp(self):
        self.db = manager.db

    def test_update_user_checked(self):
        user =  usermappers.Userclient(client_id=1, is_checked='N')
        self.db.session.add(user)
        self.db.session.commit()
        usermappers.Userclient.updateUserChecked(1)
        # Verificar que el estado se haya actualizado a 'Y'
        updated_user =  usermappers.Userclient.query.filter_by(client_id=1).first()
        assert updated_user.is_checked == 'Y'

    def test_update_nonexistent_user(self):
        # Intentar actualizar un usuario que no existe
        usermappers.Userclient.updateUserChecked(9999999)
        updated_user =  usermappers.Userclient.query.filter_by(client_id=999).first()
        self.assertIsNone(updated_user)

    def test_load_unchecked_users(self):
        user1 =  usermappers.User(username="user1", password="password1", email="user1@example.com")
        user2 =  usermappers.User(username="user2", password="password2", email="user2@example.com")
        userclient1 =  usermappers.Userclient(client_id=1, is_checked='N')
        userclient2 =  usermappers.Userclient(client_id=2, is_checked='Y')

        self.db.session.add(user1)
        self.db.session.add(user2)
        self.db.session.add(userclient1)
        self.db.session.add(userclient2)
        self.db.session.commit()

        # Llama a la función y verifica que devuelve la lista correcta de usuarios no verificados
        result = usermappers.Userclient.loadUncheckedUsers()
        expected_result = [['user1', 'password1', 'user1@example.com', 1]]

        self.assertListEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

# class DBTests(unittest.TestCase):
#     def test_user_query():
#         print(User.query.all())