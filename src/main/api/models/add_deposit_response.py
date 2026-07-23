from src.main.api.models.base_model import BaseModel


class AddDepositResponse(BaseModel):
    id: int
    balance: float
