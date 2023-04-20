import sqlalchemy.exc
from telegram.ext import CommandHandler, Application
from Scripts.db import db_session
from Scripts.db.users import User
from Scripts.db.money_update import money_update


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

async def test(update, context):
    user_id = update.message.from_user.id
    money_update(user_id, 1000)

def main():
    db_session.global_init("Data/db/users.db")
    TOKEN = '6248300309:AAFnPOsUdjAov1y3F99rpOY5BieLxDZT8qY'
    proxy_url = "socks5://user:pass@host:port"
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('test', test))
    application.run_polling()


if __name__ == '__main__':
    main()