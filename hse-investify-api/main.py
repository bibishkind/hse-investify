import asyncio

from fastapi import FastAPI, HTTPException, BackgroundTasks
import trading_view
import schemas
from schemas import NotificationAdd
from database import engine, SessionLocal
from models import Base, Notification
import crud

Base.metadata.create_all(bind=engine)

db = SessionLocal()
app = FastAPI()


async def watch(notification):
    while True:
        notification = db.query(Notification).where(Notification.id == notification.id).first()
        if notification is None:
            return
        current_indicator_value = trading_view.get_info_by_ticker(notification.ticker)[notification.indicator_name]
        if notification.expected_indicator_value >= notification.initial_indicator_value and current_indicator_value >= notification.expected_indicator_value:
            notification.active = True
            db.commit()
            print("here")
            return
        if notification.expected_indicator_value <= notification.initial_indicator_value and current_indicator_value <= notification.expected_indicator_value:
            notification.active = True
            print("here")
            db.commit()
            return
        print("doing")
        await asyncio.sleep(5)


@app.post("/notifications")
async def add_notification(notification_add: NotificationAdd, background_tasks: BackgroundTasks):
    notification = Notification()
    notification.ticker = notification_add.ticker
    notification.chat_id = notification_add.chat_id
    if notification_add.indicator_name in trading_view.AVAILABLE_INDICATORS:
        notification.indicator_name = notification_add.indicator_name
    else:
        raise HTTPException(status_code=404, detail="Indicator not found")
    notification.initial_indicator_value = trading_view.get_info_by_ticker(notification_add.ticker)[
        notification.indicator_name]
    notification.expected_indicator_value = notification_add.expected_indicator_value
    crud.add_notification(db, notification)
    background_tasks.add_task(watch, notification)


@app.get("/notifications", response_model=list[schemas.NotificationGet])
def get_notifications(active: bool | None = False):
    notifications = crud.get_active_notifications_and_delete(db) if active else crud.get_notifications(db)
    return notifications


@app.put("/notifications/{notification_id}")
def update_notification(notification_id: int, notification_update: schemas.NotificationUpdate):
    crud.update_notification(db, notification_id, notification_update.ticker, notification_update.indicator_name,
                             notification_update.expected_indicator_value)


@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int):
    crud.delete_notification(db, notification_id)

@app.get("/indicators")
def get_indicators():
    return trading_view.AVAILABLE_INDICATORS