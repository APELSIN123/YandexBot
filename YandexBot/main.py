import sqlalchemy.exc
import logging
from telegram.ext import CommandHandler, Application, CallbackQueryHandler, ConversationHandler
from Scripts.db import db_session
from Scripts.db.users import User
from Scripts.db.money_update import money_update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from mg import get_map_cell
inline_kb = [[InlineKeyboardButton('/play', callback_data='play'),
              InlineKeyboardButton('/info', callback_data='info'),
              InlineKeyboardButton('/help', callback_data='help')]]
inline_markup = InlineKeyboardMarkup(inline_kb)
inline_kb1 = [[InlineKeyboardButton('/maze', callback_data='maze'),
               InlineKeyboardButton('/durak', callback_data='durak')]]
inline_markup1 = InlineKeyboardMarkup(inline_kb1)
inline_kb2 = [[InlineKeyboardButton('/play', callback_data='play'),
              InlineKeyboardButton('/help', callback_data='help')]]
inline_markup2 = InlineKeyboardMarkup(inline_kb2)
inline_kb3 = [[InlineKeyboardButton('/play', callback_data='play'),
              InlineKeyboardButton('/info', callback_data='info')]]
inline_markup3 = InlineKeyboardMarkup(inline_kb3)
START_ROUTES, END_ROUTES = range(2)

keyboard = [[InlineKeyboardButton('←', callback_data='left'),
            InlineKeyboardButton('↑', callback_data='up'),
            InlineKeyboardButton('↓', callback_data='down'),
            InlineKeyboardButton('→', callback_data='right')]]
markup = InlineKeyboardMarkup(keyboard)

cols, rows = 6, 6
maps = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


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

        await update.message.reply_html(rf'Привет, {tguser.mention_html()}!' 
                                        f' Начнем игру? Или же хочешь сначала что-нибудь узнать?',
                                        reply_markup=inline_markup)

    except sqlalchemy.exc.IntegrityError:
        await update.message.reply_html(rf'Привет, {tguser.mention_html()}!'
                                        f' Начнем игру? Или же хочешь сначала что-нибудь узнать?',
                                        reply_markup=inline_markup)
        return START_ROUTES


async def test(update, context):
    user_id = update.message.from_user.id
    money_update(user_id, 1000)


async def info(update, context):
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text('Я - Бот для игр. Пока у меня только две игры на выбор '
                                        '- это карточный Дурак и лабиринт.\n'
                                        'Играя в них, вы будете получать или терять монеты.\n'
                                        'Вначале я дам тебе стартовый капитал - 500.\n'
                                        'А по команде /help ты узнаешь описание каждой команды. \n'
                                        'На этом всё! Удачи тебе!', reply_markup=inline_markup2)
    else:
        await update.message.reply_text('Я - Бот для игр. Пока у меня только две игры на выбор '
                                        '- это карточный Дурак и лабиринт.\n'
                                        'Играя в них, вы будете получать или терять монеты.\n'
                                        'Вначале я дам тебе стартовый капитал - 500 монет.\n'
                                        'А по команде /help ты узнаешь описание каждой команды. \n'
                                        'На этом всё! Удачи тебе!', reply_markup=inline_markup2)
    return START_ROUTES


async def play(update, context):
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text('Во что ты хочешь сыграть? Лабиринт или Дурак?', reply_markup=inline_markup1)
    else:
        await update.message.reply_text('Во что ты хочешь сыграть? Лабиринт или Дурак?', reply_markup=inline_markup1)
    return START_ROUTES


async def help1(update, context):
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text('/play - Выбор игры. \n'
                                       '/info - Краткая сводка по боту. \n'
                                       '/maze - Игра лабиринт. Деньги не нужны, за победу - 500 монет. Откат - 12ч. \n'
                                       '/durak - Игра Дурак. Минимум 2 игрока, мин. ставка - 100. \n'
                                       '/earn - Заработок монет. Даёт 250 монет. Откат 6ч. \n',
                                       reply_markup=inline_markup3)
    else:
        await update.message.reply_text('/play - Выбор игры. \n'
                                        '/info - Краткая сводка по боту. \n'
                                        '/maze - Игра лабиринт. Деньги не нужны, за победу - 500 монет. Откат - 12ч. \n'
                                        '/durak - Игра Дурак. Минимум 2 игрока, мин. ставка - 100. \n'
                                        '/earn - Заработок монет. Даёт 250 монет. Откат 6ч. \n',
                                        reply_markup=inline_markup3)
    return START_ROUTES


def get_map_str(map_cell, player):
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += "🔴"
            else:
                map_str += "⬜"
        map_str += "\n"
    return map_str


async def maze(update, context):
    map_cell = get_map_cell(cols, rows)

    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }

    query = update.callback_query
    if query:
        maps[query.message.chat_id] = user_data
        await query.answer()
        await query.message.reply_text(get_map_str(map_cell, (0, 0)), reply_markup=markup)
    else:
        maps[update.message.chat_id] = user_data
        await update.message.reply_text(get_map_str(map_cell, (0, 0)), reply_markup=markup)
    return END_ROUTES


async def callback_func(update, context):
    query = update.callback_query
    user_data = maps[query.message.chat_id]
    new_x, new_y = user_data['x'], user_data['y']

    if query.data == 'left':
        new_x -= 1
    if query.data == 'right':
        new_x += 1
    if query.data == 'up':
        new_y -= 1
    if query.data == 'down':
        new_y += 1

    if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
        return None
    if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
        return None

    user_data['x'], user_data['y'] = new_x, new_y

    if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
        query.edit_message_text(chat_id=query.message.chat_id,
                                message_id=query.message.message_id,
                                text="Вы выиграли" )
        return None

    query.edit_message_text(chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            text=get_map_str(user_data['map'], (new_x, new_y)),
                            reply_markup=markup)


async def durak(update, context):
    pass


def main():
    db_session.global_init("Data/db/users.db")
    TOKEN = '6248300309:AAFnPOsUdjAov1y3F99rpOY5BieLxDZT8qY'
    proxy_url = "socks5://user:pass@host:port"
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(play, pattern="^" + 'play' + "$"),
                CallbackQueryHandler(info, pattern="^" + 'info' + "$"),
                CallbackQueryHandler(help1, pattern="^" + 'help' + '$'),
                CallbackQueryHandler(maze, pattern="^" + 'maze' + '$'),
                CallbackQueryHandler(durak, pattern="^" + 'durak' + '$')
            ],
            END_ROUTES: [
                CallbackQueryHandler(callback_func)
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )
    application.add_handler(CommandHandler('test', test))
    application.add_handler(CommandHandler('info', info))
    application.add_handler(CommandHandler('play', play))
    application.add_handler(CommandHandler('help', help1))
    application.add_handler(CommandHandler('maze', maze))
    application.add_handler(CommandHandler('durak', durak))
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()

