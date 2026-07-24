from src.main.api.db.crud.base_crud import BaseCrud
from src.main.api.db.models.account_table import Account


class AccountCrudDb(BaseCrud[Account]):
    model = Account
