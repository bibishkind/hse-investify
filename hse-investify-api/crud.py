from models import Notification
from sqlalchemy import delete


def add_notification(db, notification):
    db.add(notification)
    db.commit()


def get_notifications(db):
    return db.query(Notification).all()


def get_active_notifications_and_delete(db):
    stmt = Notification.__table__.delete(). \
        where(Notification.active). \
        returning(Notification)

    results = db.execute(stmt).fetchall()
    print(results)
    db.commit()
    return results

def update_notification(db, notification_id, ticker, indicator_name, expected_indicator_value):
    old_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    old_notification.ticker = ticker
    old_notification.indicator_name = indicator_name
    old_notification.expected_indicator_value = expected_indicator_value
    db.commit()


def delete_notification(db, notification_id):
    notifications = db.query(Notification).all()
    db.query(Notification).filter(Notification.id == notification_id).delete()
    db.commit()
    return notifications
