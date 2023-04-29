from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


PLAYERS, BET = 1, 2
player_count, bet, deck_size = 2, 100, 36


async def durak_players(update, _):
    tguser = update.effective_user

    keyboard = [[InlineKeyboardButton('2', callback_data=2),
                 InlineKeyboardButton('3', callback_data=3),
                 InlineKeyboardButton('4', callback_data=4),
                 InlineKeyboardButton('5', callback_data=5),
                 InlineKeyboardButton('6', callback_data=6)]]

    await update.message.reply_html(
                                    rf'Привет, {tguser.mention_html()}! Давай начнём игру! Сколько игроков будет в игре?',
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    return 1


async def durak_bet(update, _):
    query = update.callback_query
    await query.answer()

    global player_count
    player_count = query.data

    keyboard = [[
                 InlineKeyboardButton('100', callback_data=100),
                 InlineKeyboardButton('250', callback_data=250),
                 InlineKeyboardButton('500', callback_data=500),
                 InlineKeyboardButton('1000', callback_data=1000),
                 InlineKeyboardButton('2500', callback_data=2500),
                 InlineKeyboardButton('5000', callback_data=5000)
                ], [
                 InlineKeyboardButton('10k', callback_data=10000),
                 InlineKeyboardButton('25k', callback_data=25000),
                 InlineKeyboardButton('50k', callback_data=50000),
                 InlineKeyboardButton('100k', callback_data=1000),
                 InlineKeyboardButton('250k', callback_data=2500),
                 InlineKeyboardButton('500k', callback_data=5000)
                ], [
                 InlineKeyboardButton('1m', callback_data=1000000),
                 InlineKeyboardButton('2,5m', callback_data=2500000),
                 InlineKeyboardButton('5m', callback_data=5000000),
                 InlineKeyboardButton('10m', callback_data=10000000),
                 InlineKeyboardButton('25m', callback_data=25000000),
                 InlineKeyboardButton('50m', callback_data=50000000)
                 ]]

    await query.message.reply_text(
                                   f"Отлично! А на сколько будем играть?",
                                   reply_markup=InlineKeyboardMarkup(keyboard)
                                   )

    return 2


async def durak_deck(update, _):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton('36', callback_data=36),
                 InlineKeyboardButton('52', callback_data=52)]]

    global player_count
    if int(player_count) <= 4:
        keyboard[0].insert(0, InlineKeyboardButton('24', callback_data=24))

    await query.message.reply_text('Очень хорошо! Сколько карт будет в колоде?', reply_markup=InlineKeyboardMarkup(keyboard))

    return 3


async def stop(update, _):
    return ConversationHandler.END