from .users import User
from . import db_session

def win_lose_update(id, arg):
    db_session.global_init("Data/db/users.db")
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.id == id).first()
    if arg == 'win':
        user.count_wins += 1
    else:
        user.count_loses += 1

    db_sess.commit()