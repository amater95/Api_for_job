import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_fixture import transfer_data_request
from src.main.api.models.add_deposit_request import AddDepositRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.test_data.invalid_test_data import InvalidTestData
from src.main.api.test_data.error_messages import ErrorMessages
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.test_data.test_data import TestData


@pytest.mark.api
class TestTransfer:
    def test_transfer_to_yourself(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_with_money_request: AddDepositRequest, transfer_data_request: TransferRequest):
        response = api_manager.user_steps.transfer_to_yourself(create_user_request, transfer_data_request)

        account_from = Account.get_one_from_db(db_session, id = transfer_data_request.fromAccountId)

        assert response.fromAccountIdBalance == create_account_with_money_request.balance - transfer_data_request.amount, (
            f"Баланс на счете {transfer_data_request.fromAccountId} должен быть {create_account_with_money_request.balance - transfer_data_request.amount}, а не {response.fromAccountIdBalance}"
        )
        assert account_from.balance == create_account_with_money_request.balance - transfer_data_request.amount, f"На счете осталась некорректная сумма"


    @pytest.mark.parametrize("transfer", InvalidTestData.INVALID_DATA_FOR_TRANSFER)
    def test_transfer_to_yourself_invalid_summ(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, create_account_request, create_account_with_money_request: AddDepositRequest, transfer_data_request: TransferRequest, transfer: float):
        invalid_transfer_request = transfer_data_request
        invalid_transfer_request.amount = transfer
        response = api_manager.user_steps.transfer_to_yourself_invalid_summ(create_user_request, invalid_transfer_request)

        account_to = Account.get_one_from_db(db_session, id = transfer_data_request.toAccountId)

        assert response.json()["error"] == ErrorMessages.INVALID_TRANSFER_AMOUNT, f"Ожидалась ошибка {ErrorMessages.INVALID_TRANSFER_AMOUNT}, а была получена {response.json()["error"]}"
        assert account_to.balance == TestData.START_DEPOSIT_AMOUNT, "Сумма на счете была пополнена и не равна 0"
