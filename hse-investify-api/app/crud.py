# crud.py
import logging
from models.models import Notification

def add_notification(db, notification):
    logging.info("db add notification")
    db.add(notification)
    db.commit()

def get_notifications(db):
    logging.info("db get notifications")
    return db.query(Notification).all()

def get_active_notifications(db):
    logging.info("db get active notifications")
    return db.query(Notification).where(Notification.active).all()

def update_notification(db, notification):
    logging.info("db update notification")
    updated_notification = db.query(Notification).filter(Notification.id == notification.id).first()
    updated_notification.ticker = notification.ticker
    updated_notification.indicator_name = notification.indicator_name
    updated_notification.expected_indicator_value = notification.expected_indicator_value
    db.commit()

def delete_notifications(db):
    logging.info("db delete notifications")
    db.query(Notification).delete()
    db.commit()

def delete_active_notifications(db):
    logging.info("db delete active notifications")
    db.query(Notification).where(Notification.active).delete()
    db.commit()

def delete_notification(db, id):
    logging.info("db delete notification")
    db.query(Notification).where(Notification.id == id).delete()
    db.commit()
