from typing import Annotated

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class TransferRequest(BaseModel):
    fromAccountId: int
    toAccountId: int
    amount: Annotated[float, CreationRule(regex=r'^(500(\.\d{2})?|[1-8]\d{3}(\.\d{2})?|10000(\.00)?)$')]
