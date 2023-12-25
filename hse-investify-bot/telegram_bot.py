import telebot
from telebot import types
import requests
import threading
import time
from urllib.parse import urlencode
from config import options, TOKEN, start_url, help_info

tb = telebot.TeleBot(token=TOKEN, parse_mode=None)
notification = {"chat_id": 0, "ticker": "", "indicator_name": "", 'expected_indicator_value': 0.0}
to_change = 0
indicators = requests.get(start_url + "indicators").json()


def set_menu_keyboard(variants):
    menu = types.InlineKeyboardMarkup(row_width=4)
    for i in variants:
        button = types.InlineKeyboardButton(text=i, callback_data=variants[i])
        menu.add(button)
    return menu


def ask(call, text, next_step):
    if call:
        message = call.message
        chat_id = call.from_user.id
    else:
        message = call
        chat_id = message.chat.id
    reply_required = types.ForceReply(selective=False)
    tb.send_message(chat_id, text, reply_markup=reply_required)
    tb.register_next_step_handler(message, next_step)


@tb.callback_query_handler(func=lambda call: call.data == "get_indicators")
def get_tech_indicators(call):
    menu = set_menu_keyboard(options)
    ind_list = "Список доступных индикаторов:\n"
    for i in indicators:
        ind_list += f"{i}\n"
    tb.send_message(call.from_user.id, ind_list, reply_markup=menu, parse_mode='Markdown')


def get_info_by_ticker(ticker):
    # menu = set_menu_keyboard(options)
    # try:
    #     #info = get_info_by_ticker(ticker.text)
    #     text = ticker.text + '\n'
    #     for i in info:
    #         text += i + ' = '
    #         text += str(info[i]) + '\n'
    #     tb.send_message(ticker.chat.id, text, reply_markup=menu)
    # except Exception as e:
    #     tb.send_message(ticker.chat.id, "Ошибка")
    return


@tb.callback_query_handler(func=lambda call: call.data[:4] == "make" or call.data == "info")
def ask_ticker(call):
    if len(call.data) > 4:
        global to_change
        to_change = call.data[4:]
    if call.data == "info":
        ask(call, "Введите тикер:", get_info_by_ticker)
    else:
        ask(call, "Введите тикер:", ask_indicator)


def ask_indicator(ticker):
    notification['ticker'] = ticker.text.upper()
    indicators_menu = types.InlineKeyboardMarkup(row_width=2)
    for i in range(len(indicators)):
        button = types.InlineKeyboardButton(text=indicators[i], callback_data=f"indicator{i}")
        indicators_menu.add(button)
    tb.send_message(ticker.chat.id, "Выберите индикатор:", reply_markup=indicators_menu)


@tb.callback_query_handler(func=lambda call: call.data[:9] == "indicator")
def ask_notification_value(call):
    notification['indicator_name'] = indicators[int(call.data[9:])]
    ask(call, "Введите ожидаемое значение:", create_notification)


def create_notification(value):
    menu = set_menu_keyboard(options)
    notification['chat_id'] = value.chat.id
    try:
        notification['expected_indicator_value'] = float(value.text)
    except ValueError:
        tb.send_message(value.chat.id, "Некорректное значение", reply_markup=menu)
        return
    global to_change
    action = "создано"
    if to_change:
        c = requests.put(start_url + f"notifications/{to_change}", json=notification)
        to_change = 0
        action = "изменено"
    else:
        c = requests.post(start_url + "notifications", json=notification)
    if c.status_code == 200:
        tb.send_message(value.chat.id, f"Уведомление {action}", reply_markup=menu)
    else:
        tb.send_message(value.chat.id, "Ошибка", reply_markup=menu)


@tb.callback_query_handler(func=lambda call: call.data == "notification_list")
def get_notification_list(call):
    chat_id = call.from_user.id
    menu = set_menu_keyboard(options)
    resp = requests.get(start_url + "notifications?" + urlencode({'active': 'false'})).json()
    n_list = "Список текущих уведомлений:\n"
    j = 1
    for i in resp:
        if i['chat_id'] == chat_id:
            n_list += (f"{j}) Тикер: *{i['ticker']}*\nИндикатор:\n     *{i['indicator_name']}*\n"
                       f"Ожидаемое значение: *{i['expected_indicator_value']}*\n\n")
            j += 1
    if j == 1:
        tb.send_message(chat_id, "Список уведомлений пуст", reply_markup=menu)
        return
    tb.send_message(chat_id, n_list, parse_mode='Markdown')


def set_notification_menu(resp, chat_id, next_step):
    notification_menu = types.InlineKeyboardMarkup(row_width=7)
    is_empty = True
    for i in resp:
        if i['chat_id'] == chat_id:
            button = types.InlineKeyboardButton(
                text=f"Тикер: {i['ticker']}, индикатор: {i['indicator_name']},"
                     f" ожидаемое значение: {i['expected_indicator_value']}\n",
                callback_data=f"{next_step}{i['id']}")
            notification_menu.add(button)
            is_empty = False
    return (notification_menu, is_empty)


@tb.callback_query_handler(func=lambda call: call.data == "change")
def change_notification(call):
    chat_id = call.from_user.id
    resp = requests.get(start_url + "notifications?" + urlencode({'active': 'false'})).json()
    notification_menu, is_empty = set_notification_menu(resp, chat_id, 'make')
    if is_empty:
        menu = set_menu_keyboard(options)
        tb.send_message(chat_id, "Список уведомлений пуст", reply_markup=menu)
    else:
        tb.send_message(chat_id, "Выберите уведомление, которое хотите изменить:", reply_markup=notification_menu)


@tb.callback_query_handler(func=lambda call: call.data[:6] == "delete")
def delete_notification(call):
    chat_id = call.from_user.id
    if len(call.data) > 6:
        to_delete = call.data[6:]
        c = requests.delete(start_url + f"notifications/{to_delete}")
        menu = set_menu_keyboard(options)
        if c.status_code == 200:
            tb.send_message(chat_id, "Уведомление удалено", reply_markup=menu)
        else:
            tb.send_message(chat_id, "Ошибка", reply_markup=menu)
    else:
        resp = requests.get(start_url + "notifications?" + urlencode({'active': 'false'})).json()
        notification_menu, is_empty = set_notification_menu(resp, chat_id, 'delete')
        if is_empty:
            menu = set_menu_keyboard(options)
            tb.send_message(chat_id, "Список уведомлений пуст", reply_markup=menu)
        else:
            tb.send_message(chat_id, "Выберите уведомление, которое хотите удалить:", reply_markup=notification_menu)


@tb.callback_query_handler(func=lambda call: call.data == "clear")
def clear_notifications(call):
    menu = set_menu_keyboard(options)
    chat_id = call.from_user.id
    status_code1 = requests.delete(start_url + "notifications?" + urlencode({'active': 'true'}))
    status_code2 = requests.delete(start_url + "notifications?" + urlencode({'active': 'false'}))
    tb.send_message(chat_id, "Все уведомления удалены", reply_markup=menu)


@tb.message_handler(regexp=".")
def show_menu(message):
    menu = set_menu_keyboard(options)
    tb.send_message(message.chat.id, "Меню:", reply_markup=menu)


@tb.callback_query_handler(func=lambda call: call.data == "help")
def info(call):
    menu = set_menu_keyboard(options)
    tb.send_message(call.from_user.id, help_info, reply_markup=menu, parse_mode="Markdown")


def infinity_requesting():
    while True:
        url = start_url + "notifications?" + urlencode({'active': 'true'})
        resp = requests.get(url).json()
        requests.delete(url)
        for n in resp:
            tb.send_message(n['chat_id'], f"*Уведомление по тикеру {n['ticker']} по "
                            f"индикатору {n['indicator_name']} со "
                            f"значением {n['expected_indicator_value']} сработало!*", parse_mode="Markdown")
        time.sleep(10)


thread1 = threading.Thread(target=infinity_requesting)
thread2 = threading.Thread(target=tb.infinity_polling)
thread1.start()
thread2.start()
thread1.join()
thread2.join()