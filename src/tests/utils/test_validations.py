import unittest
from src.utils import validations as vld


class TestVerificationAlgorithms(unittest.TestCase):
    def test_verification_date_good(self):
        self.assertEqual(vld.validate_date("2023-11-19"), True)

    def test_verification_date_bad(self):
        self.assertEqual(vld.validate_date("19-2023-11"), False)
        self.assertEqual(vld.validate_date("19-11-2023"), False)
        self.assertEqual(vld.validate_date("aaaaaaaaa"), False)
        self.assertEqual(vld.validate_date("2023/11/19"), False)

    def test_verification_password_good(self):
        self.assertEqual(vld.validate_password("Holamundo1234@"), True)

    def test_verification_password_bad(self):
        self.assertEqual(vld.validate_password("1234"), False)
        self.assertEqual(vld.validate_password("HolaMundo1234"), False)
        self.assertEqual(vld.validate_password("HolaMundo@"), False)
        self.assertEqual(vld.validate_password("HolaMundo123@"), False)
        self.assertEqual(vld.validate_password("molamundo1234@"), False)

    def test_verification_email_good(self):
        self.assertEqual(vld.validate_email("email@dominio.com"), True)

    def test_verification_email_bad(self):
        self.assertEqual(vld.validate_email("email"), False)
        self.assertEqual(vld.validate_email("email@dominio"), False)
        self.assertEqual(vld.validate_email("email@dominio."), False)
        self.assertEqual(vld.validate_email("email@.com"), False)
        self.assertEqual(vld.validate_email("email@dominio..com"), False)
        self.assertEqual(vld.validate_email("email@@dominio.com"), False)
        self.assertEqual(vld.validate_email("email@."), False)
        self.assertEqual(vld.validate_email("@dominio.com"), False)
        self.assertEqual(vld.validate_email("email@dominio.c"), False)
        self.assertEqual(vld.validate_email(""), False)
