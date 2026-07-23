from sqlalchemy.orm import Session

from src.main.api.db.crud.base_crud import BaseCrud
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb(BaseCrud[Transaction]):
    model = Transaction

    @classmethod
    def get_transaction_by_same_id(cls, db: Session, to_account_id: int, from_account_id: int) -> Transaction | None:
        return (db.query(cls.model).filter(cls.model.to_account_id == to_account_id, cls.model.from_account_id == from_account_id).order_by(cls.model.created_at.desc()).first())
