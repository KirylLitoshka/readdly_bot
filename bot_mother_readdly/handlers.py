from aiogram import Bot, Dispatcher, types

links = {
    "lina": "https://t.me/denise_el_patrona_bot?start=user_from_motherbot",
    "photo": "https://t.me/bruna_el_patrona_bot?start=user_from_motherbot",
    "anime": "https://t.me/rena_el_patrona_bot?start=user_from_motherbot"
}


async def create_new_user(user_id, users_storage):
    users_storage[str(user_id)] = {
        "gender": None,
        "picture_type": None,
        "current_choices": "gender"
    }


async def show_menu(message: types.Message):
    await message.answer(
        text="""
        Hola! Elige una de las historias e inicia un diálogo interactivo
        1. <b>Una noche solitaria</b> — Una noche solitaria en el hostal donde trabaja Reina, en una compañía intimidante.
        2. <b>Atención a las señales</b> — Una madre soltera que se va a trabajar deja a sus hijas en casa donde ocurren cosas que hielan la sangre.
        3. <b>Alguien observando</b> — Es un momento terrible para un fin de semana de acampada en familia, ya que están siendo atacados.
        4. <b>El trén a ningún lado</b> — ¿A dónde llevará a Josh el viaje en el tren vacío?
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
