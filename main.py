import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from api.get_data import get_price, get_tokens, get_info, get_top10, get_top_exchanges
from config_data.config import BOT_TOKEN
import text
from base import insert_info, insert_top, insert_price, get_base, get_base_2, insert_top_ex

bot = telebot.TeleBot(BOT_TOKEN)


def create_keyboard(page=0, per_page=25, call="crypto_", call_next="navigater_"):
    """
    :param call_next: callback_data для переключения страниц
    :param call: callback_data для поиска криптовалюты
    :param page: номер страницы
    :param per_page: количество символов на странице
    :return: клавиатура
    """
    keyboard = InlineKeyboardMarkup()
    data = get_tokens()
    keys = list(data.keys())
    start = page * per_page
    end = start + per_page
    for i in range(start, min(end, len(keys)), 5):
        row = [InlineKeyboardButton(text=f"{keys[j].upper()}", callback_data=f"{call}{data[keys[j]]}") for j in
               range(i, min(i + 5, len(keys)))]
        keyboard.row(*row)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️Назад", callback_data=f"{call_next}{str(page - 1)}"))
    if end < len(keys):
        nav_buttons.append(InlineKeyboardButton("Далее➡️", callback_data=f"{call_next}{str(page + 1)}"))
    keyboard.row(*nav_buttons)
    return keyboard


@bot.message_handler(commands=['start'])
def welcome(message: Message):
    information_message = bot.send_message(chat_id=message.chat.id, text=text.welcome(message.from_user.first_name))
    bot.delete_message(chat_id=message.from_user.id, message_id=information_message.message_id - 1)


@bot.message_handler(commands=['price'])
def price(message: Message):
    keyboard = create_keyboard(page=0)
    information_message = bot.send_message(
        message.chat.id,
        "Выберете криптовалюту:",
        reply_markup=keyboard
    )
    bot.delete_message(chat_id=message.from_user.id, message_id=information_message.message_id - 1)


@bot.callback_query_handler(func=lambda call: call.data.startswith("crypto_") or call.data.startswith("navigate_"))
def handle_query(call: CallbackQuery):
    if call.data.startswith("crypto_"):
        token = call.data.split("_")[1]
        information_message = bot.send_message(call.message.chat.id, get_price(token))
        bot.delete_message(chat_id=call.from_user.id, message_id=information_message.message_id - 1)
        insert_price(call.from_user.id, token)
    elif call.data.startswith("navigate_"):
        page = int(call.data.split("_")[1])
        keyboard = create_keyboard(page=page)
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)


@bot.message_handler(commands=['info'])
def price(message: Message):
    keyboard = create_keyboard(page=0, call="cryptor_", call_next="navigater_")
    information_message = bot.send_message(
        message.chat.id,
        "Выберете криптовалюту:",
        reply_markup=keyboard
    )
    bot.delete_message(chat_id=message.from_user.id, message_id=information_message.message_id - 1)


@bot.callback_query_handler(func=lambda call: call.data.startswith("cryptor_") or call.data.startswith("navigater_"))
def handle_query(call: CallbackQuery):
    if call.data.startswith("cryptor_"):
        token = call.data.split("_")[1]
        textt, image = get_info(token)
        try:
            information_message = bot.send_photo(chat_id=call.from_user.id, photo=image, caption=textt)
        except:
            information_message = bot.send_message(chat_id=call.from_user.id, text=textt)
        bot.delete_message(chat_id=call.from_user.id, message_id=information_message.message_id-1)
        insert_info(call.from_user.id, token)
    elif call.data.startswith("navigater_"):
        page = int(call.data.split("_")[1])
        keyboard = create_keyboard(page=page, call="cryptor_", call_next="navigater_")
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)


@bot.message_handler(commands=['top'])
def top10(message: Message):
    keyboard = InlineKeyboardMarkup()
    nav_buttons = []
    nav_buttons.append(InlineKeyboardButton("Далее➡️", callback_data=f"navitg_1"))
    keyboard.row(*nav_buttons)
    information_message = bot.send_photo(chat_id=message.from_user.id, caption=get_top10()[0][0], photo=get_top10()[1][0], reply_markup=keyboard)
    bot.delete_message(chat_id=message.from_user.id, message_id=information_message.message_id - 1)
    insert_top(message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("navitg_"))
def top10_0(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    keyboardrr = InlineKeyboardMarkup()
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️Назад", callback_data=f"navitg_{page - 1}"))
    if page < 9:
        nav_buttons.append(InlineKeyboardButton("Далее➡️", callback_data=f"navitg_{page + 1}"))
    keyboardrr.row(*nav_buttons)
    try:
        information_message = bot.send_photo(chat_id=callback.from_user.id, caption=get_top10()[0][page], photo=get_top10()[1][page], reply_markup=keyboardrr)
    except:
        information_message = bot.send_message(chat_id=callback.from_user.id, text=get_top10()[0][page], reply_markup=keyboardrr)
    bot.delete_message(chat_id=callback.from_user.id, message_id=information_message.message_id - 1)


@bot.message_handler(commands=['top_exchanges'])
def top_exchanges(message: Message):
    keyboard = InlineKeyboardMarkup()
    nav_buttons = []
    nav_buttons.append(InlineKeyboardButton("Далее➡️", callback_data=f"nav_ex_1"))
    keyboard.row(*nav_buttons)
    information_message = bot.send_photo(chat_id=message.from_user.id, caption=get_top_exchanges()[0][0], photo=get_top_exchanges()[1][0], reply_markup=keyboard)
    bot.delete_message(chat_id=message.from_user.id, message_id=information_message.message_id - 1)
    insert_top_ex(message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("nav_ex_"))
def top_exchanges_0(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    keyboardrr = InlineKeyboardMarkup()
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️Назад", callback_data=f"nav_ex_{page - 1}"))
    if page < 9:
        nav_buttons.append(InlineKeyboardButton("Далее➡️", callback_data=f"nav_ex_{page + 1}"))
    keyboardrr.row(*nav_buttons)
    try:
        information_message = bot.send_photo(chat_id=callback.from_user.id, caption=get_top_exchanges()[0][page], photo=get_top_exchanges()[1][page], reply_markup=keyboardrr)
    except:
        information_message = bot.send_message(chat_id=callback.from_user.id, text=get_top_exchanges()[0][page], reply_markup=keyboardrr)
    bot.delete_message(chat_id=callback.from_user.id, message_id=information_message.message_id - 1)


@bot.message_handler(commands=['history'])
def history(message: Message):
    lst = get_base(message.from_user.id)
    if len(lst) == 0:
        information_message = bot.send_message(chat_id=message.from_user.id, text="К сожалению, вы ничего не искали в нашем боте.")
    else:
        keyboard = InlineKeyboardMarkup()
        for i in range(0, len(lst), 2):
            nav_buttons = []
            nav_buttons.append(InlineKeyboardButton(text=lst[i][1], callback_data=f"histo_" + str(lst[i][1])))
            try:
                nav_buttons.append(InlineKeyboardButton(text=lst[i+1][1], callback_data=f"histo_" + str(lst[i+1][1])))
            except:
                pass
            keyboard.row(*nav_buttons)
        information_message = bot.send_message(chat_id=message.from_user.id, text="Выберете дату:", reply_markup=keyboard)
    bot.delete_message(chat_id=message.from_user.id, message_id=information_message.message_id - 1)


@bot.callback_query_handler(func=lambda call: call.data == "go_back")
def history(callback: CallbackQuery):
    lst = get_base(callback.from_user.id)
    if len(lst) == 0:
        information_message = bot.send_message(chat_id=callback.from_user.id, text="К сожалению, вы ничего не искали в нашем боте.")
    else:
        keyboard = InlineKeyboardMarkup()
        for i in range(0, len(lst), 2):
            nav_buttons = []
            nav_buttons.append(InlineKeyboardButton(text=lst[i][1], callback_data=f"histo_" + str(lst[i][1])))
            try:
                nav_buttons.append(InlineKeyboardButton(text=lst[i+1][1], callback_data=f"histo_" + str(lst[i+1][1])))
            except:
                pass
            keyboard.row(*nav_buttons)
        information_message = bot.send_message(chat_id=callback.from_user.id, text="Выберете дату:", reply_markup=keyboard)
    bot.delete_message(chat_id=callback.from_user.id, message_id=information_message.message_id-1)


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] == "histo")
def histo_dd(callback: CallbackQuery):
    info = get_base_2(callback.from_user.id, callback.data.split("_")[1])
    date = info[1]
    com = info[2]
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text="Назад", callback_data="go_back")
    keyboard.add(back_button)
    crypto = info[3]
    if com == "top10":
        ttrext = f"{date}\n\nТоп 10 криптовалют по капитализации в валюте."
    elif com == "info":
        ttrext = f"{date}\n\nПоиск информации о {crypto}"
    elif com == "top_ex":
        ttrext = f"{date}\n\nТоп 10 криптобирж"
    else:
        ttrext = f"{date}\n\nСтоимость {crypto}"
    information_message = bot.send_message(chat_id=callback.from_user.id, text=ttrext, reply_markup=keyboard)
    bot.delete_message(chat_id=callback.from_user.id, message_id=information_message.message_id-1)


@bot.message_handler(commands=['help'])
def cmd_help(message: Message):
    information_message = bot.send_message(chat_id=message.from_user.id, text=text.help())
    bot.delete_message(chat_id=message.from_user.id, message_id=information_message.message_id - 1)


@bot.message_handler()
def other(message: Message):
    bot.send_message(chat_id=message.from_user.id, text="Оу, такой команды нет(")


if __name__ == '__main__':
    print('Бот запущен!')
    bot.polling(none_stop=True)
