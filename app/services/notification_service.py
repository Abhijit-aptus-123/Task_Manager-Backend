from app.db.models import Notification

def create_notification(db, user_id, message):
    notification = Notification(
        user_id=user_id,
        message=message,
        is_read="false"
    )
    db.add(notification)
    db.commit()


def get_user_notifications(db, user_id):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.timestamp.desc()).all()


def mark_as_read(db, notification_id, user_id):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()

    if notification:
        notification.is_read = "true"
        db.commit()

    return notification