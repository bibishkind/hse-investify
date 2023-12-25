# schemas.py
from pydantic import BaseModel

class NotificationsPost(BaseModel):
    chat_id: int
    ticker: str
    indicator_name: str
    expected_indicator_value: float

class NotificationsGet(BaseModel):
    id: int
    chat_id: int
    ticker: str
    indicator_name: str
    expected_indicator_value: float
    active: bool

class NotificationsPut(BaseModel):
    ticker: str
    indicator_name: str
    expected_indicator_value: float

class InformationGet(BaseModel):
    ticker: str
    name: str
    price: float
    currency: str
    exchange: str
