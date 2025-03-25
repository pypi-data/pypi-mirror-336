from .delete_email import sync as delete_email
from .delete_email import asyncio as delete_email_async
from .get_email_by_id import sync as get_email_by_id
from .get_email_by_id import asyncio as get_email_by_id_async

__all__ = [
    "delete_email",
    "delete_email_async",
    "get_email_by_id",
    "get_email_by_id_async",
]
