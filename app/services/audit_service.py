from sqlalchemy.orm import Session, joinedload
from app.db.models import AuditLog, User


# ======================
# CREATE AUDIT LOG
# ======================
def log_action(db: Session, user_id, action, resource, resource_id):

    log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id
    )

    db.add(log)
    db.commit()


# ======================
# GET AUDIT LOGS (UPDATED)
# ======================
def get_audit_logs(db: Session):

    logs = (
        db.query(AuditLog)
        .options(joinedload(AuditLog.user))  # JOIN USER
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    result = []

    for log in logs:
        result.append({
            "id": log.id,
            "email": log.user.email if log.user else None,  # EMAIL INSTEAD
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "timestamp": log.timestamp
        })

    return result