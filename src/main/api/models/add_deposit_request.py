from typing import Annotated

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class AddDepositRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(regex=r'^(?:(?:[1-8]\d{3})\.\d{2}|9000\.00)$')]
