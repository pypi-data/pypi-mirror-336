from datetime import datetime
from uuid import UUID

from ed_domain.entities.notification import NotificationType


class NotificationModel:
    user_id: UUID
    notification_type: NotificationType
    message: str
    created_datetime: datetime
