import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.test_data.error_messages import ErrorMessages
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.test_data.test_data import TestData


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_full(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_repay_data_request: CreditRepayRequest):
        response = api_manager.user_steps.credit_repay_full(create_credit_user_request, credit_repay_data_request)

        transaction_from_db = Transaction.get_one_from_db(db_session, credit_id = credit_repay_data_request.creditId)
        credit_from_db = Credit.get_one_from_db(db_session, account_id = credit_repay_data_request.accountId)

        assert response.creditId == credit_repay_data_request.creditId, (
            f"Id кредитного счета {response.creditId} не соответствует с ожидаемым {credit_repay_data_request.creditId}"
        )
        assert response.amountDeposited == credit_repay_data_request.amount, (
            f"Сумма погашения кредита {credit_repay_data_request.amount} должна быть = {response.amountDeposited}"
        )
        assert transaction_from_db is not None, "Не найдено записи транзакции погашения"
        assert transaction_from_db.transaction_type == TestData.TRANSACTION_TYPE_CREDIT_REPAY, "Транзакция не классифицирована как погашение кредита"
        assert credit_from_db.balance == TestData.START_DEPOSIT_AMOUNT, "Кредит не был погашен"


    def test_credit_repay_unfull(self, db_session: Session, api_manager:ApiManager, create_credit_user_request: CreateUserRequest, create_account_with_credit_request, credit_repay_invalid_data_request: CreditRepayRequest):
        response = api_manager.user_steps.credit_repay_unfull(create_credit_user_request, credit_repay_invalid_data_request)

        transaction_from_db = Transaction.get_one_from_db(db_session, credit_id = credit_repay_invalid_data_request.creditId)
        credit_from_db = Credit.get_one_from_db(db_session, account_id = credit_repay_invalid_data_request.accountId)

        assert response.json()["error"] == ErrorMessages.DONT_FULL_SUMM_CREDIT.format(credit_summ = int(create_account_with_credit_request.amount)), (
            f"Ожидалась ошибка {ErrorMessages.DONT_FULL_SUMM_CREDIT.format(credit_summ = int(create_account_with_credit_request.amount))}, "
            f"была получена {response.json()["error"]}"
        )
        assert transaction_from_db is None, "В БД создалась запись на погашение кредита с невалидным значением суммы"
        assert credit_from_db.balance == - create_account_with_credit_request.amount, "Сумма кредита изменилась"
