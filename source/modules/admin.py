import users
from users import CompanyUser


users = CompanyUser.query.all()
for user in users:
    print(user.username, user.password, user.email)


