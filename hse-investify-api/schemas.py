from pydantic import BaseModel


class NotificationAdd(BaseModel):
    chat_id: int
    ticker: str
    indicator_name: str
    expected_indicator_value: float


class NotificationGet(BaseModel):
    id: int
    chat_id: int
    ticker: str
    indicator_name: str
    # current_indicator_value: float
    expected_indicator_value: float


class NotificationUpdate(BaseModel):
    ticker: str
    indicator_name: str
    expected_indicator_value: float
