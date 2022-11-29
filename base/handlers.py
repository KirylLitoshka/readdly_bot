from aiogram import Dispatcher, types

from base.utils.choices import on_choice_action
from base.utils.messages import sending_messages_till_answer


async def create_new_user(dp_data, user_id, username):
    dp_data["users"][user_id] = dp_data["default_user_model"].copy()
    dp_data["users"][user_id].update({
        "id": user_id,
        "username": username.title(),
        "referral_type": dp_data["users"][user_id].get("referral_type")
    })


async def echo(message: types.Message):
    dispatcher = Dispatcher.get_current()
    user_id = str(message.from_user.id)
    if user_id not in dispatcher.data["users"]:
        await create_new_user(dispatcher.data, user_id, message.from_user.first_name)
        if len(message.text.split()) != 1:
            if message.text.startswith("/start"):
                dispatcher.data["users"][user_id]["referral_type"] = message.text.split()[1]
                message.text = message.text.split()[0]
    current_user = dispatcher.data["users"][user_id]
    possible_answers = current_user["registered_answers"]
    answer_texts = [item["text"] for item in possible_answers]
    if message.text not in answer_texts:
        await dispatcher.bot.delete_message(message.chat.id, message.message_id)
        return
    current_user["registered_answers"] = []
    choice_index = answer_texts.index(message.text)
    if possible_answers[choice_index]["on_choice"]:
        on_choice_expression = possible_answers[choice_index]["on_choice"]
        on_choice_action(current_user, on_choice_expression)
    next_dialog_id = possible_answers[choice_index]["next_id"]
    current_user["last_received_message_id"] = next_dialog_id
    try:
        await sending_messages_till_answer(dispatcher, current_user, user_id, next_dialog_id)
    except KeyError:
        await back_to_root_bot(message)
        return


async def back_to_root_bot(message: types.Message):
    msg = "Gracias por leer.\nMás historias en @ReaddlyProject_bot 🕷"
    inline_keyboard = types.InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Seleccione la historia",
                    url="https://t.me/ReaddlyProject_bot",
                )
            ]
        ],
    )
    await message.answer(
        text=msg,
        reply_markup=inline_keyboard,
    )


async def restart(query: types.CallbackQuery):
    user_id = str(query.from_user.id)
    dispatcher = Dispatcher.get_current()
    await create_new_user(dispatcher.data, user_id, dispatcher.data["users"][user_id]["username"])
    current_user = dispatcher.data["users"][user_id]
    await sending_messages_till_answer(dispatcher, current_user, user_id, "0")
