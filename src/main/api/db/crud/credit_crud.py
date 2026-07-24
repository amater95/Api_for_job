from src.main.api.db.crud.base_crud import BaseCrud
from src.main.api.db.models.credit_table import Credit


class CreditCrudDb(BaseCrud[Credit]):
    model = Credit
