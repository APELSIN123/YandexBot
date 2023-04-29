from Scripts.DB import db_session
from Scripts.DB.users import User
import sqlalchemy.exc


async def start(update, context):
    tguser = update.effective_user
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name

    try:
        user = User()
        user.id = int(user_id)
        user.name = user_name
        user.count_wins = 0
        user.count_loses = 0
        user.money = 0

        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()

        await update.message.reply_html(rf'Привет, {tguser.mention_html()}! Я запомнил тебя!')

    except sqlalchemy.exc.IntegrityError:
        await update.message.reply_html(rf'Привет, {tguser.mention_html()}! Я уже тебя знаю!')