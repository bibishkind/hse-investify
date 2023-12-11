import telebot
from telebot import types
import requests
import threading
import time


tb = telebot.TeleBot(token='', parse_mode=None)
options = {"Добавить уведомление": "make",
           "Посмотреть список уведомлений": "notification_list",
           "Получить список индикаторов": "get_indicators",
           "Изменить уведомление": "change",
           "Удалить уведомление": "delete",
           "Удалить все уведомления": "clear"}
notification = {"chat_id": 1, "ticker": "", "indicator_name": "", 'expected_indicator_value': 0.0}
to_change = 0
indicators = requests.get(f"http://localhost:8000/indicators").json()



def set_menu_keyboard(variants):
    menu = types.InlineKeyboardMarkup(row_width=2)
    for i in variants:
        button = types.InlineKeyboardButton(text=i, callback_data=variants[i])
        menu.add(button)
    return menu

markup2 = set_menu_keyboard(options)


def ask(call, text, next_step):
    if call:
        message = call.message
    else:
        message = call
    markup = types.ForceReply(selective=False)
    tb.send_message(message.chat.id, text, reply_markup=markup)
    tb.register_next_step_handler(message, next_step)


@tb.message_handler(commands=['start'])
def send_menu(message):
    markup = set_menu_keyboard(options)
    tb.send_message(message.chat.id, "Меню:", reply_markup=markup)


@tb.callback_query_handler(func=lambda call: call.data == "get_indicators")
def send_tech_indicators(call):
    markup = set_menu_keyboard(options)
    ind_list = "Список доступных индикаторов:\n"
    for i in indicators:
        ind_list += i + '\n'
    tb.send_message(call.message.chat.id, ind_list, reply_markup=markup2)

# @tb.callback_query_handler(func=lambda call: call.data == "get")
# def send_tech_indicators(call):
#     ask(call, "Введите тикер:", get_info)
#
# def get_info(ticker):
#     markup = set_menu_keyboard(options)
#     try:
#         info = get_info_by_ticker(ticker.text)
#         text = ticker.text.upper() + '\n'
#         for i in info:
#             text += i + ' = '
#             text += str(info[i]) + '\n'
#         tb.send_message(ticker.chat.id, text, reply_markup=markup)
#     except Exception as e:
#         tb.send_message(ticker.chat.id, "Ошибка")
#         print(e)




@tb.callback_query_handler(func=lambda call: call.data[:4] == "make")
def ask_ticker(call):
    if len(call.data) > 4:
        global to_change
        to_change = call.data[4:]
    notification['chat_id'] = call.message.chat.id
    ask(call, "Введите тикер:", show_indicators_menu)


def show_indicators_menu(ticker):
    notification['ticker'] = ticker.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in range(len(indicators)):
        button = types.InlineKeyboardButton(text=indicators[i], callback_data=f"indicator{i}")
        markup.add(button)
    tb.send_message(ticker.chat.id, "Выберите индикатор:", reply_markup=markup)


@tb.callback_query_handler(func=lambda call: call.data[:9] == "indicator")
def ask_notification_value(call):
    notification['indicator_name'] = indicators[int(call.data[9:])]
    ask(call, "Введите ожидаемое значение:", get_notification_value)


def get_notification_value(value):
    markup = set_menu_keyboard(options)
    try:
        notification['expected_indicator_value'] = float(value.text)
    except ValueError:
        tb.send_message(value.chat.id, "Некорректное значение", reply_markup=markup)
        return
    global to_change
    action = "создано"
    if to_change:
        c = requests.put(f"http://localhost:8000/notifications/{to_change}", json=notification)
        to_change = 0
        action = "изменено"
    else:
        c = requests.post("http://localhost:8000/notifications", json=notification)
    if c.status_code == 200:
        tb.send_message(value.chat.id, f"Уведомление {action}", reply_markup=markup)
    else:
        tb.send_message(value.chat.id, "Ошибка", reply_markup=markup)


@tb.callback_query_handler(func=lambda call: call.data == "notification_list")
def get_notification_list(call):
    message = call.message
    markup = set_menu_keyboard(options)
    resp = requests.get(f"http://localhost:8000/notifications").json()
    if len(resp) == 0:
        tb.send_message(message.chat.id, "Список уведомлений пуст", reply_markup=markup)
        return
    n_list = "Список текущих уведомлений:\n"
    j = 1
    for i in resp:
        n_list += (f"{j}) Тикер: {i['ticker'].upper()}\n     Индикатор: {i['indicator_name']}\n     "
                   f"Ожидаемое значение: {i['expected_indicator_value']}\n")
        j += 1
    tb.send_message(message.chat.id, n_list, reply_markup=markup)


@tb.callback_query_handler(func=lambda call: call.data == "change")
def choose_notification_to_change(call):
    message = call.message
    resp = requests.get(f"http://localhost:8000/notifications").json()
    if len(resp) == 0:
        markup = set_menu_keyboard(options)
        tb.send_message(message.chat.id, "Список уведомлений пуст", reply_markup=markup)
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in resp:
        button = types.InlineKeyboardButton(
            text=f"Тикер: {i['ticker']}, индикатор: {i['indicator_name']},"
                 f" ожидаемое значение: {i['expected_indicator_value']}\n",
            callback_data=f"make{i['id']}")
        markup.add(button)
    tb.send_message(message.chat.id, "Выберите уведомление, которое хотите изменить:", reply_markup=markup)


@tb.callback_query_handler(func=lambda call: call.data[:6] == "delete")
def choose_notification_to_delete(call):
    message = call.message
    if len(call.data) > 6:
        to_delete = call.data[6:]
        c = requests.delete(f"http://localhost:8000/notifications/{to_delete}")
        markup = set_menu_keyboard(options)
        if c.status_code == 200:
            tb.send_message(message.chat.id, "Уведомление удалено", reply_markup=markup)
        else:
            tb.send_message(message.chat.id, "Ошибка", reply_markup=markup)
    else:
        resp = requests.get(f"http://localhost:8000/notifications").json()
        if len(resp) == 0:
            markup = set_menu_keyboard(options)
            tb.send_message(message.chat.id, "Список уведомлений пуст", reply_markup=markup)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        for i in resp:
            button = types.InlineKeyboardButton(
                text=f"Тикер: {i['ticker']}, индикатор: {i['indicator_name']},"
                     f"ожидаемое значение: {i['expected_indicator_value']}\n",
                callback_data=f"delete{i['id']}")
            markup.add(button)
        tb.send_message(message.chat.id, "Выберите уведомление, которое хотите удалить:", reply_markup=markup)



@tb.callback_query_handler(func=lambda call: call.data == "clear")
def clear_notifications(call):
    markup = set_menu_keyboard(options)
    message = call.message
    resp = requests.get(f"http://localhost:8000/notifications").json()
    status = "Все уведомления удалены"
    for i in resp:
        if i['chat_id'] == message.chat.id:
            c = requests.delete(f"http://localhost:8000/notifications/{i['id']}")
            if c.status_code != 200:
                status = "Ошибка"
    tb.send_message(message.chat.id, status, reply_markup=markup)


@tb.message_handler(regexp=".")
def echo(message):
    tb.send_message(message.chat.id, message.text)


def infinity_requesting():
    while True:
        resp = requests.get(f"http://localhost:8000/notifications?active=True").json()
        for n in resp:
            tb.send_message(n['chat_id'], f"Уведомление по тикеру {n['ticker'].upper()} по "
                                       f"индикатору {n['indicator_name']} со "
                                       f"значением {n['expected_indicator_value']} сработало!")
        time.sleep(60)


thread1 = threading.Thread(target=infinity_requesting)
thread2 = threading.Thread(target=tb.infinity_polling)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
