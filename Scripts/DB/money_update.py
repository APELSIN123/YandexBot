from .users import User
from . import db_session

def money_update(id, amount):
    db_session.global_init("Data/DB/users.DB")
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.id == id).first()
    user.money += amount
    print(f'{user.name} earned {amount} money, now his money is {user.money}')

    db_sess.commit()