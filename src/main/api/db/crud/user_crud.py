from src.main.api.db.crud.base_crud import BaseCrud
from src.main.api.db.models.user_table import User


class UserCrudDb(BaseCrud[User]):
    model = User
