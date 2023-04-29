from Scripts.DB.money_update import money_update


async def test(update, context):
    user_id = update.message.from_user.id
    money_update(user_id, 1000)