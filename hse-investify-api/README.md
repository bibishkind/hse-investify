# hse-invsitfy-api

Это API для взаимодействия с уведомлениями на основе технических индикаторов. Он использует FastAPI и SQLAlchemy для базы данных и извлекает данные из Trading View (клиент реализован) для предоставления уведомлений в реальном времени.

## Начало работы

Для запуска проекта вам необходимо создать файл .env со следующим содержимым:
DATABASE_URL = postgresql://postgres:postgres@localhost:5432/postgres

Затем установите необходимые пакеты из requirements.txt.

Затем запустите контейнер Docker с базой данных с помощью следующей команды:
docker run -d --name hse-investify-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres


Наконец, запустите API с помощью следующей команды:
uvicorn main:app


## Доступные методы API

- **GET /indicators**: Получить список доступных индикаторов.
- **POST /notifications**: Добавить новое уведомление. Пример тела запроса: { chat_id:, ticker:, indicator_name:, expected_indicator_value:  }
- **GET /notifications**: Получить все уведомления. Добавление параметра запроса active=true вернет все активные уведомления (готовые к отправке пользователям). Сервер удалит эти уведомления из базы данных после их возврата.
- **PUT /notifications/{notification_id}**: Обновить уведомление. Пример тела запроса: { ticker:, indicator_name:, expected_indicator_value:}
- **DELETE /notifications/{notification_id}**: Удалить уведомление.

## Пример файла .env
DATABASE_URL = postgresql://postgres:postgres@localhost:5432/postgres


## Зависимости
- FastAPI
- SQLAlchemy
- Docker
- Trading View API

## Участники
- Денис
- Настя

## Лицензия
Этот проект лицензирован в соответствии с лицензией MIT - см. файл [LICENSE](LICENSE) для получения дополнительной информации.