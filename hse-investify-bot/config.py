options = {"Добавить уведомление": "make",
           "Получить информацию по акции": "info",
           "Посмотреть список уведомлений": "notification_list",
           "Получить список индикаторов": "get_indicators",
           "Изменить уведомление": "change",
           "Удалить уведомление": "delete",
           "Удалить все уведомления": "clear",
           "Помощь": "help"}
TOKEN = ''
start_url = "http://localhost:8000/"
help_info = ("_Бот предоставляет следующие возможности:_\n\n     "
             "- *Добавить уведомление* (потребуется ввести тикер, индикатор и значение индикатора, по "\
             "достижению которого вам будет отправлено уведомление)\n\n    "\
             "- *Получить информацию по акции* (получение текущих значений технических индикаторов по тикеру)\n\n    "\
             "- *Посмотреть список уведомлений* (посмотреть список уже созданных уведомлений)\n\n    "\
             "- *Получить список индикаторов* (посмотреть список доступных технических индикаторов)\n\n    "
             "- *Изменить уведомление* (выбрать уведомление из уже созданных и изменить)\n\n    "
             "- *Удалить уведомление/все уведомления*\n\n"
             "*Меню отображается при отправке боту любого сообщения (кроме случаев, когда бот требует ввести "
             "тикер или значение)*")