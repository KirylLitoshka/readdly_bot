import aiofiles
import json
from datetime import datetime
from aiogram import Bot, Dispatcher, types

links = {
    "lina": "https://t.me/denise_el_patrona_bot?start=user_from_motherbot",
    "photo": "https://t.me/bruna_el_patrona_bot?start=user_from_motherbot",
    "anime": "https://t.me/rena_el_patrona_bot?start=user_from_motherbot"
}


def get_referral_type(message: str):
    sequence = message.split()
    if len(sequence) > 1:
        return sequence[1]
    return None


async def save_user(dp: Dispatcher, user: dict):
    user_id = user["id"]
    dp.data['users'][user_id] = user
    async with aiofiles.open(f'{dp.data["storage"]}/users/{user_id}.json', mode="w") as fp:
        await fp.write(json.dumps(user, indent=4, ensure_ascii=False))


async def create_new_user(message: types.Message):
    user_id = str(message.from_user.id)
    current_time = datetime.strftime(datetime.utcnow(), "%s")
    dp = Dispatcher.get_current()
    user_ref = get_referral_type(message.text)
    if user_id in dp.data["users"]:
        return
    user = {
        "id": user_id,
        "referral_type": user_ref,
        "created": current_time
    }
    await save_user(dp, user)


async def show_menu(message: types.Message):
    await create_new_user(message)
    await message.answer(
        text="""
Hola! Elige una de las historias e inicia un diálogo interactivo

<b>📚 Una noche solitaria</b>
📃 Una noche solitaria en el hostal donde trabaja Reina, en una compañía intimidante.

<b>📚 Atención a las señales</b>
📃 Una madre soltera que se va a trabajar deja a sus hijas en casa donde ocurren cosas que hielan la sangre.

<b>📚 Alguien observando</b>
📃 Es un momento terrible para un fin de semana de acampada en familia, ya que están siendo atacados.

<b>📚 El trén a ningún lado</b>
📃 ¿A dónde llevará a Josh el viaje en el tren vacío?
        """,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="Una noche solitaria",
                    url="https://t.me/Reina_ReaddlyProject_bot?start=user_from_motherbot"
                )],
                [types.InlineKeyboardButton(
                    text="Atención a las señales",
                    url="https://t.me/Lina_ReaddlyProject_bot?start=user_from_motherbot"
                )],
                [types.InlineKeyboardButton(
                    text="Alguien observando",
                    url="https://t.me/Krystal_ReaddlyProject_bot?start=user_from_motherbot"
                )],
                [types.InlineKeyboardButton(
                    text="El trén a ningún lado",
                    url="https://t.me/Josh_ReaddlyProject_bot?start=user_from_motherbot"
                )],
            ],

            resize_keyboard=True,
            one_time_keyboard=True
        ),
        parse_mode="HTML"
    )
