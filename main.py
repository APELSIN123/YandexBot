from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, InlineQueryHandler
from telegram.ext import Updater, MessageHandler, filters

from Scripts.DB import db_session
from Scripts.Commands import start, test, durak
from Durak.game import init_game, join, run_game


def main():
    db_session.global_init("Data/db/users.db")
    TOKEN = '6248300309:AAFnPOsUdjAov1y3F99rpOY5BieLxDZT8qY'
    proxy_url = "socks5://user:pass@host:port"
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start.start))
    application.add_handler(CommandHandler('test', test.test))
    application.add_handler(CommandHandler('join', join))

    conv_handler = ConversationHandler(entry_points=[CommandHandler('durak', durak.durak_players)],

                                       states=

                                        {
                                         1: [CallbackQueryHandler(durak.durak_bet)],
                                         2: [CallbackQueryHandler(durak.durak_deck)],
                                         3: [CallbackQueryHandler(init_game)],
                                         4: [CallbackQueryHandler(run_game)]
                                        },

                                       fallbacks=[CommandHandler('stop', durak.stop)])

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()