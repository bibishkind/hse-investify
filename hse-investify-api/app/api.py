# api.py
from fastapi import FastAPI, HTTPException
from . import schemas
import logging
from models.models import Notification
from trading_view import trading_view
from . import crud
from .db import db

api = FastAPI()

@api.post("/notifications")
def post_notifications(notifications_post: schemas.NotificationsPost):
    logging.info("api post notifications")
    notification = Notification()
    notification.ticker = notifications_post.ticker
    notification.chat_id = notifications_post.chat_id
    if notifications_post.indicator_name in trading_view.AVAILABLE_INDICATORS:
        notification.indicator_name = notifications_post.indicator_name
    else:
        raise HTTPException(status_code=404)
    notification.initial_indicator_value = trading_view.get_info(notifications_post.ticker)[
        notifications_post.indicator_name]
    notification.expected_indicator_value = notifications_post.expected_indicator_value
    crud.add_notification(db, notification)

@api.get("/notifications", response_model=list[schemas.NotificationsGet])
def get_notifications(active: bool | None):
    logging.info("api get notifications")
    notifications = crud.get_notifications(db)
    for notification in notifications:
        current_indicator_value = trading_view.get_info(notification.ticker)[notification.indicator_name]
        if notification.initial_indicator_value <= notification.expected_indicator_value <= current_indicator_value:
            notification.active = True
            db.commit()
        if notification.initial_indicator_value >= notification.expected_indicator_value >= current_indicator_value:
            notification.active = True
            db.commit()
    if active:
        return crud.get_active_notifications(db)
    else:
        return crud.get_notifications(db)

@api.put("/notifications/{id}")
def put_notifications(id: int, notifications_put: schemas.NotificationsPut):
    logging.info("api put notifications")
    notification = Notification()
    notification.id = id
    notification.ticker = notifications_put.ticker
    if notifications_put.indicator_name in trading_view.AVAILABLE_INDICATORS:
        notification.indicator_name = notifications_put.indicator_name
    else:
        raise HTTPException(status_code=404)
    notification.initial_indicator_value = trading_view.get_info(notifications_put.ticker)[
        notifications_put.indicator_name]
    notification.expected_indicator_value = notifications_put.expected_indicator_value
    crud.update_notification(db, notification)

@api.delete("/notifications")
def delete_notifications(active: bool | None):
    logging.info("api delete notifications")
    if active:
        crud.delete_active_notifications(db)
    else:
        crud.get_active_notifications(db)

@api.delete("/notifications/{id}")
def delete_notifications(id: int):
    logging.info("api delete notifications")
    crud.delete_notification(db, id)

@api.get("/indicators", response_model=list[str])
def get_indicators():
    logging.info("api get indicators")
    return trading_view.AVAILABLE_INDICATORS

@api.get("/information/{ticker}", response_model=[schemas.InformationGet])
def get_information(ticker: str):
    return trading_view.get_search(ticker)
