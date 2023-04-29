import json

from .Classes.game import Game

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

players = []
game = None



async def join(update, context):
    global players
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    chat = str(update.message.chat.id)
    players.append((user_id, user_name, chat))
    print('/join ok')


async def init_game(update, context):
    from Scripts.Commands.durak import player_count, bet, deck_size
    global players

    query = update.callback_query

    chat = str(query.message.chat.id)

    file = open(f'Durak/{chat.strip()}_game', encoding='utf-8', mode='w')
    data = {'player_count': player_count,
            'bet': bet,
            'deck_size': deck_size,
            'player_0': (query.from_user.id, query.from_user.username)}

    for i in range(int(player_count) - 1):
        player = players[i]
        if player[2] == chat and player[:-1] not in data:
            data[f'player_{i + 1}'] = tuple(player[:-1])

    json.dump(data, file)

    await query.message.reply_text(f'Игра создана успешно! Игроки: {" ".join([str(data[f"player_{i}"][1]) for i in range(int(player_count))])}. \n'
                                   f'Ставка: {bet}. \n  Колода на {deck_size}')





    return 4


async def run_game(update, context):
    from Scripts.Commands.durak import player_count, bet, deck_size
    from decks import small_deck, basic_deck, poker_deck
    global game

    player_count = int(player_count)

    if deck_size == 24:
        deck = small_deck
    elif deck_size == 36:
        deck = basic_deck
    elif deck_size == 52:
        deck = poker_deck

    game = Game(player_count, deck)

    query = update.callback_query
    chat = str(query.message.chat.id)

    file = open(f'Durak/{chat.strip()}_game', encoding='utf-8', mode='r')
    data = json.load(file)

    for i in range(player_count):
        game.add_player(data[f'player_{i}'][0], i)

    player_index = 0

    keyboard = [[InlineKeyboardButton(str(i), callback_data=i) for i in game.players[player_index].hand]]

    await query.message.send_message(chat_id=data[f'player_{player_index}'][0],
                                     text='Ваш ход! Выбирайте карту для хода',
                                     reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END
