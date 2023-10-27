"""
import users
from users import CompanyUser


company_users = CompanyUser.query.all()

def companyuser_info():
    company_user_dict = []

    for user in company_users:
        user_info = {
            'ID': user.companyuser_id,
            'Name': user.name,
            'NIF': user.nif,
            'Bank Account': user.bankaccount,
        }
        company_user_dict.append(user_info)

    return company_user_dict
"""
